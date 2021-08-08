import logging
from http.server import HTTPServer, SimpleHTTPRequestHandler

logger = logging.getLogger(__name__)


def start_web_server(context, port=8000):
    webroot = context.root_directory.joinpath('www/')

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
