from http.server import HTTPServer, SimpleHTTPRequestHandler

from .logger import info
from .files import join

PORT = 8000


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=join('www'), **kwargs)


def serve():
    httpd = HTTPServer(('', PORT), Handler)
    try:
        info(f'starting webserver: http://127.0.0.1:{PORT}')
        httpd.serve_forever()
    except KeyboardInterrupt:
        info('stopping web server')
        httpd.server_close()
