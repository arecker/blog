import logging
import sys

logger = logging.getLogger(__name__)


def configure_logging(verbose=False, silent=False):
    if verbose and silent:
        raise ValueError(
            'hey smartass, how am I supposed to be silent AND verbose?')

    if silent:
        logging.disable()
        return

    if verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO

    fmt = 'blog - %(levelname)s - %(name)s - %(message)s'

    logging.basicConfig(level=level, stream=sys.stderr, format=fmt)
    logger.debug('configured logging with level = %s', level)
