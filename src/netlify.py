'''
functions for working with Netlify's API
'''

import hashlib
import json
import logging
import time
import urllib.request

logger = logging.getLogger(__name__)

# curl -H 'User-Agent: MyApp (YOUR_NAME@EXAMPLE.COM)' \
#      -H 'Authorization: Bearer YOUR_OAUTH2_ACCESS_TOKEN' \
#      https://api.netlify.com/api/v1/sites


def make_request(path,
                 token='',
                 method='GET',
                 data={},
                 encoding='UTF-8',
                 content_type='application/json'):
    if not path.startswith('/'):
        path = '/' + path

    url = f'https://api.netlify.com/api/v1{path}'

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-type': content_type,
        'User-Agent': 'blog',
    }

    if data and content_type == 'application/json':
        data = json.dumps(data)
        data = data.encode(encoding)
    elif not data:
        data = None

    request = urllib.request.Request(method=method,
                                     url=url,
                                     headers=headers,
                                     data=data)
    response = urllib.request.urlopen(request)
    response_data = response.read().decode(encoding)
    return json.loads(response_data)


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

    files = list(webroot.glob('**/*.*'))
    total = len(files)
    for i, f in enumerate(files):
        key = '/' + str(f.relative_to(webroot))
        value = hash_file(f)
        digest_map[key] = value
        if (i + 1) % 500 == 0 or (i + 1) == total:
            logger.info('hashed %d of %d file(s)', i + 1, total)

    return {'files': digest_map, 'draft': False, 'async': False}


def deploy(site_name='', token='', webroot=None):
    start_time = time.time()
    site_id = fetch_site_id(site_name, token=token)
    logger.info('found netlify site %s (%s)', site_name, site_id)

    payload = build_new_deploy(webroot)
    logger.info('built payload from %d file(s) in %s',
                len(payload['files'].keys()), webroot)

    response = make_request(path=f'/sites/{site_id}/deploys/',
                            token=token,
                            method='POST',
                            data=payload)

    deploy_id = response['id']
    total = len(response['required'])
    logger.info('created deploy %s, %d file(s) need to be uploaded',
                response['id'], total)

    hash_map = dict([(v, k) for k, v in payload['files'].items()])
    for i, sha in enumerate(response['required']):
        path = hash_map[sha]
        with open(str(webroot) + path, 'rb') as f:
            data = f.read()
        url = f'/deploys/{deploy_id}/files{path}'
        response = make_request(path=url,
                                token=token,
                                method='PUT',
                                data=data,
                                content_type='application/octet-stream')
        logger.info('uploaded %s (%d/%d)', path, i + 1, total)

    logger.info('deploy finished (%d s)', time.time() - start_time)
