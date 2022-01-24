'''
serve webroot locally
'''

import logging
import pathlib
from http.server import HTTPServer, SimpleHTTPRequestHandler

from blog.commands import build

logger = logging.getLogger(__name__)
root_dir = pathlib.Path(__file__).parent.parent.parent


def start_web_server(webroot, port=8000):
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=webroot, **kwargs)

        def log_message(self, format, *args):
            logger.debug(f'{format}', *args)

    httpd = HTTPServer(('', port), Handler)
    try:
        logger.info(f'starting webserver at {webroot} - http://0.0.0.0:{port}')
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info('stopping web server')
        httpd.server_close()


def register(parser):
    build.register(parser)


def main(args):
    build.main(args)
    start_web_server(root_dir / 'www')
