'''
serve webroot locally
'''

import logging
from http.server import HTTPServer, SimpleHTTPRequestHandler

from src.commands import build

logger = logging.getLogger(__name__)


def start_web_server(webroot, port=8000):
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=webroot, **kwargs)

        def log_message(self, format, *args):
            logger.debug(f'{format}', *args)

    httpd = HTTPServer(('', port), Handler)
    try:
        logger.info(f'starting webserver - http://0.0.0.0:{port}')
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info('stopping web server')
        httpd.server_close()


def main(args):
    build.main(args)
    start_web_server(args.root_directory / 'www')
