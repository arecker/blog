import logging
import os
import sys


logger = logging.getLogger('blog')


def enable_logger():
    global logger
    log_level = logging.getLevelName(os.environ.get('LOG_LEVEL', 'INFO').upper())
    logger.setLevel(log_level)
    logger.handlers = []
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
    logger.addHandler(handler)
