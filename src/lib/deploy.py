"""Deploy site to Netlify"""

import hashlib
import json
import logging
import pathlib
import time
import urllib.parse

from . import http

logger = logging.getLogger(__name__)


def make_request(path,
                 token='',
                 method='GET',
                 data={},
                 encoding='UTF-8',
                 content_type='application/json'):

    if not path.startswith('/'):
        path = '/' + path

    url = f'https://api.netlify.com/api/v1{path}'

    return http.make_http_request(url=url,
                                  method=method,
                                  authorization=f'Bearer {token}',
                                  data=data,
                                  content_type=content_type)


def fetch_site_id(site_name, token=''):
    data = make_request('/sites', token=token)

    for result in data:
        if site_name == result['custom_domain']:
            return result['id']

    raise ValueError(f'Couldn\'t find ID for site "{site_name}"')


def hash_file(path, buffer_size=65536):
    sha1 = hashlib.sha1()

    with open(path, 'rb') as f:
        while True:
            data = f.read(buffer_size)
            if not data:
                break
            sha1.update(data)

    return str(sha1.hexdigest())


def build_new_deploy(webroot):
    digest_map = {}

    files = [p for p in webroot.glob('**/*') if p.is_file()]
    total = len(files)
    for i, f in enumerate(files):
        key = '/' + str(f.relative_to(webroot))
        value = hash_file(f)
        digest_map[key] = value
        if (i + 1) % 500 == 0 or (i + 1) == total:
            logger.info('hashed %d of %d file(s)', i + 1, total)

    return {'files': digest_map, 'draft': False, 'async': False}


def read_netlify_token(secrets_dir):
    with (pathlib.Path(secrets_dir) / 'netlify.json').open('r') as f:
        return json.load(f)['token']


def deploy_to_netlify(full_url='', secrets_dir='', www_dir='', dry=False):
    domain = urllib.parse.urlparse(full_url).netloc
    token = read_netlify_token(secrets_dir)

    site_id = fetch_site_id(domain, token=token)
    logger.info('found netlify site %s (%s)', domain, site_id)
    dir_www = pathlib.Path(www_dir).absolute()
    payload = build_new_deploy(dir_www)
    logger.info('built payload from %d file(s) in %s',
                len(payload['files'].keys()), str(dir_www))

    if dry:
        logger.warn('running in dry mode, can\'t proceed with deploy')
        return

    response = make_request(path=f'/sites/{site_id}/deploys/',
                            token=token,
                            method='POST',
                            data=payload)

    deploy_id = response['id']
    total = len(response['required'])
    logger.info('created deploy %s, %d file(s) need to be uploaded',
                response['id'], total)

    hash_map = dict([(v, k) for k, v in payload['files'].items()])
    required = sorted(response['required'], key=lambda r: hash_map[r])
    for i, sha in enumerate(required):
        path = hash_map[sha]
        with open(str(dir_www) + path, 'rb') as f:
            data = f.read()
        url = f'/deploys/{deploy_id}/files{path}'
        response = make_request(path=url,
                                token=token,
                                method='PUT',
                                data=data,
                                content_type='application/octet-stream')

        logger.info('uploaded %s (%d/%d)', path, i + 1, total)

    max_seconds = 120
    seconds = max_seconds

    while True:
        response = make_request(path=f'/deploys/{deploy_id}',
                                token=token,
                                method='GET')
        status = response['state']

        logger.info('deploy %s is in status "%s" (%d/%ds)', deploy_id, status,
                    seconds, max_seconds)

        if status == 'ready':
            break

        if seconds > 0:
            seconds = seconds - 1
            time.sleep(1)
        else:
            raise RuntimeError('timeout for netlify deploy %s exceeded',
                               deploy_id)

    logger.info('deploy %s finished!', deploy_id)