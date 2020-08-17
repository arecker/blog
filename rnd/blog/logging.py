import logging
import os
import sys


logger = logging.getLogger('blog')


def enable_logger(verbose=False):
    global logger

    if verbose:
        log_level = logging.getLevelName('DEBUG')
    else:
        log_level = logging.getLevelName('INFO')

    logger.setLevel(log_level)
    logger.handlers = []
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
    logger.addHandler(handler)
