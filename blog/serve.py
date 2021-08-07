import logging
from http.server import HTTPServer, SimpleHTTPRequestHandler

logger = logging.getLogger(__name__)


def start_web_server(directory, port=8000):
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=directory, **kwargs)

        def log_message(self, format, *args):
            logger.debug(f'{format}', *args)

    httpd = HTTPServer(('', port), Handler)
    try:
        logger.info(f'starting webserver - http://0.0.0.0:{port}')
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info('stopping web server')
        httpd.server_close()
