import json
import urllib.request


def make_http_request(url: str,
                      method: str = 'GET',
                      data: str | dict = None,
                      authorization: str = '',
                      content_type: str = 'application/json',
                      encoding: str = 'UTF-8'):
    """Issue an HTTP request to a URL and decode the respsonse."""

    headers = {
        'Content-type': content_type,
        'User-Agent': 'blog',
    }

    if data and content_type == 'application/json':
        data = json.dumps(data)
        data = data.encode(encoding)

    if authorization:
        headers['Authorization'] = authorization

    request = urllib.request.Request(url=url,
                                     headers=headers,
                                     method=method,
                                     data=data)

    response = urllib.request.urlopen(request)
    response_data = response.read().decode(encoding)

    try:
        response_data = json.loads(response_data)
    except json.decoder.JSONDecodeError:
        pass

    return response_data
