import argparse
import blog
import logging
import platform

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('-v',
                    '--verbose',
                    action='store_true',
                    help='show debug logs')


def main():
    """Run main CLI routine."""

    args = parser.parse_args()
    blog.configure_logging(verbose=args.verbose)

    logger.debug('running blog with python v%s', platform.python_version())


if __name__ == '__main__':
    main()
