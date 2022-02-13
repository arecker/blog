"""deploy site to Netlify"""

import hashlib
import logging
import time

from . import http, build

logger = logging.getLogger(__name__)


def register(subparser):
    subparser.add_argument('--netlify-token',
                           required=True,
                           help='Netlify API token')
    build.register(subparser)


def make_request(path,
                 token='',
                 method='GET',
                 data={},
                 encoding='UTF-8',
                 content_type='application/json'):

    if not path.startswith('/'):
        path = '/' + path

    url = f'https://api.netlify.com/api/v1{path}'

    return http.make_request(url=url,
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


def main(args):
    build.main(args)

    domain = args.full_url.netloc
    site_id = fetch_site_id(domain, token=args.netlify_token)
    logger.info('found netlify site %s (%s)', domain, site_id)

    payload = build_new_deploy(args.directory / 'www')
    logger.info('built payload from %d file(s) in %s',
                len(payload['files'].keys()), args.directory / 'www')

    response = make_request(path=f'/sites/{site_id}/deploys/',
                            token=args.netlify_token,
                            method='POST',
                            data=payload)

    deploy_id = response['id']
    total = len(response['required'])
    logger.info('created deploy %s, %d file(s) need to be uploaded',
                response['id'], total)

    hash_map = dict([(v, k) for k, v in payload['files'].items()])
    for i, sha in enumerate(response['required']):
        path = hash_map[sha]
        with open(str(args.directory / 'www') + path, 'rb') as f:
            data = f.read()
        url = f'/deploys/{deploy_id}/files{path}'
        response = make_request(path=url,
                                token=args.netlify_token,
                                method='PUT',
                                data=data,
                                content_type='application/octet-stream')

        logger.info('uploaded %s (%d/%d)', path, i + 1, total)

    max_seconds = 120
    seconds = max_seconds

    while True:
        response = make_request(path=f'/deploys/{deploy_id}',
                                token=args.netlify_token,
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
