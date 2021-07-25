import logging
import sys

import blog

logger = logging.getLogger(__name__)


def main():
    """The main routine.

    Parse global args and call the right function based on the
    subcommand.
    """

    default_config_path = str(blog.root_directory.joinpath('blog.conf'))

    # Parse arguments
    parser = blog.build_argparser(default_config_path)
    args = parser.parse_args()

    # Setup logging
    blog.configure_logging(verbose=args.verbose, silent=args.silent)

    logger.debug('parsed args %s', vars(args))

    # Print help if needed
    if not args.subcommand:
        parser.print_help()
        sys.exit(1)
    elif args.subcommand == 'help':
        parser.print_help()
        sys.exit(0)

    # Build config and info
    config = blog.load_config(args.config)
    info = blog.gather_build_info()

    if args.subcommand == 'render':
        result = render(args.source, config, info)
        print(result)


def render(source, config, info):
    page = blog.Page(source)

    result = blog.build_html_page(page=page, config=config, info=info)
    logger.info('rendered %s to HTML', page)
    return result


if __name__ == '__main__':
    try:
        main()
    except Exception:
        logger.exception('Unhandled exception!')
        sys.exit(1)
