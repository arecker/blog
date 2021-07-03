from http.server import HTTPServer, SimpleHTTPRequestHandler

from .logger import info
from .files import join

PORT = 8000


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=join('www'), **kwargs)

    def log_message(self, format, *args):
        info(f'serve - {format}', *args)


def serve():
    httpd = HTTPServer(('', PORT), Handler)
    try:
        info(f'starting webserver - http://0.0.0.0:{PORT}')
        httpd.serve_forever()
    except KeyboardInterrupt:
        info('stopping web server')
        httpd.server_close()
