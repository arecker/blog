import argparse
import logging
import platform
import sys

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('-v',
                    '--verbose',
                    action='store_true',
                    help='show debug logs')


def configure_logger(verbose=False):
    kwargs = {
        'stream': sys.stderr,
        'format': '%(name)s: %(message)s',
    }

    if verbose:
        kwargs['level'] = logging.DEBUG
    else:
        kwargs['level'] = logging.INFO

    logging.basicConfig(**kwargs)


def main():
    """Run main CLI routine."""

    args = parser.parse_args()
    configure_logger(verbose=args.verbose)

    logger.debug('running blog with python v%s', platform.python_version())
