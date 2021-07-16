from http.server import HTTPServer, SimpleHTTPRequestHandler

from . import logger, root_directory


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,
                         directory=root_directory.joinpath('www/'),
                         **kwargs)

    def log_message(self, format, *args):
        logger.debug(f'{format}', *args)


def start_web_server(port=8000):
    httpd = HTTPServer(('', port), Handler)
    try:
        logger.info(f'starting webserver - http://0.0.0.0:{port}')
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info('stopping web server')
        httpd.server_close()
