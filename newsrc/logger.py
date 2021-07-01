import logging
import sys


def make_logger():
    logger = logging.getLogger('blog')
    handler = logging.StreamHandler(stream=sys.stderr)
    formatter = logging.Formatter('BLOG: %(message)s')

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    return logger


logger = make_logger()


def info(msg, *args):
    logger.info(msg, *args)


def debug(msg, *args):
    logger.debug(msg, *args)
