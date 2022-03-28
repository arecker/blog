import json
import urllib.request


def make_http_request(url: str,
                      authorization: str = '',
                      content_type: str = 'application/json',
                      encoding: str = 'UTF-8'):
    """Issue an HTTP request to a URL and decode the respsonse."""

    headers = {
        'Content-type': content_type,
        'User-Agent': 'blog',
    }

    if authorization:
        headers['Authorization'] = authorization

    request = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(request)
    response_data = response.read().decode(encoding)

    try:
        response_data = json.loads(response_data)
    except json.decoder.JSONDecodeError:
        pass

    return response_data
