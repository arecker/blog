import logging
import platform
import sys

logger = logging.getLogger(__name__)


def main():
    """Run main CLI routine."""

    logging.basicConfig(stream=sys.stderr, format='%(name)s: %(message)s', level=logging.DEBUG)

    logger.debug('running blog with python v%s', platform.python_version())
