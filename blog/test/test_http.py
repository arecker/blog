import contextlib
import unittest
import unittest.mock
import urllib.request

from blog import http


@contextlib.contextmanager
def patch_urlopen(response_data: str = ''):
    response_data = response_data.encode('UTF-8')
    response = unittest.mock.Mock(read=lambda: response_data)
    with unittest.mock.patch.object(urllib.request,
                                    'urlopen',
                                    return_value=response) as p:
        yield p


class TestHTTP(unittest.TestCase):
    def test_make_http_request(self):

        with patch_urlopen(response_data='{"hello": "world"}') as p:
            kwargs = {
                'url': 'https://www.alexrecker.com',
                'method': 'POST',
                'data': {
                    'test': True
                },
                'authorization': 'Fart Token',
            }
            response = http.make_http_request(**kwargs)

        request = p.call_args[0][0]

        self.assertEqual(request.get_full_url(), 'https://www.alexrecker.com')
        self.assertEqual(request.data.decode('UTF-8'), '{"test": true}')
        self.assertEqual(request.headers['User-agent'], 'blog')
        self.assertEqual(request.headers['Content-type'], 'application/json')
        self.assertEqual(request.headers['Authorization'], 'Fart Token')
        self.assertEqual(request.method, 'POST')
        self.assertDictEqual(response, {'hello': 'world'})

        with patch_urlopen(response_data='Everything is fine') as p:
            response = http.make_http_request(url='http://127.0.0.1')

        request = p.call_args[0][0]
        self.assertEqual(response, 'Everything is fine')
