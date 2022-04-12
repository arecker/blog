import blog
import logging
import platform
import sys

logger = logging.getLogger(__name__)


def main(args=sys.argv[1:]):
    """Run main CLI routine."""

    args = blog.parse_args(args=args)
    blog.configure_logging(verbose=args.verbose)

    logger.debug('running blog with python v%s', platform.python_version())


if __name__ == '__main__':
    main()
