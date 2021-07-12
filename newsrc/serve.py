from http.server import HTTPServer, SimpleHTTPRequestHandler

from newsrc import logger, files

PORT = 8000


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=files.join('www'), **kwargs)

    def log_message(self, format, *args):
        logger.debug(f'{format}', *args)


def start_web_server():
    httpd = HTTPServer(('', PORT), Handler)
    try:
        logger.info(f'starting webserver - http://0.0.0.0:{PORT}')
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info('stopping web server')
        httpd.server_close()
