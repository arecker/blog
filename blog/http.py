import json
import urllib.request


def make_request(url,
                 method='GET',
                 data={},
                 encoding='UTF-8',
                 authorization=None,
                 content_type='application/json'):

    headers = {
        'Content-type': content_type,
        'User-Agent': 'blog',
    }

    if authorization:
        headers['Authorization'] = authorization

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

    try:
        response_data = json.loads(response_data)
    except json.decoder.JSONDecodeError:
        pass

    return response_data
