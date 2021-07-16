import logging
import sys


def make_logger():
    """Make a copy of the blog global logger

    >>> logger = make_logger()
    """

    logger = logging.getLogger('blog')
    handler = logging.StreamHandler(stream=sys.stderr)
    formatter = logging.Formatter('blog: %(message)s')

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    return logger


logger = make_logger()
