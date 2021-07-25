import logging
import sys

import blog

logger = logging.getLogger(__name__)

SUBCOMMANDS = {
    'help': {
        'help': 'print program usage'
    },
    'render': {
        'posargs': [{
            'key': 'path',
            'type': str,
            'help': 'path to entry or page',
        }],
        'help':
        'print a rendered page'
    }
}


def main():
    """The main routine.

    Parse global args and call the right function based on the
    subcommand.
    """

    default_config_path = str(blog.root_directory.joinpath('blog.conf'))

    # Parse global arguments
    parser = blog.build_global_argparser(default_config_path,
                                         subcommands=SUBCOMMANDS)
    global_args = parser.parse_args()

    # Setup logging
    blog.configure_logging(verbose=global_args.verbose,
                           silent=global_args.silent)

    logger.debug('parsed args %s', vars(global_args))

    # Print help if needed
    if not global_args.subcommand:
        parser.print_help()
        sys.exit(1)
    elif global_args.subcommand == 'help':
        parser.print_help()
        sys.exit(0)

    # Build config
    config = blog.load_config(global_args.config)


if __name__ == '__main__':
    try:
        main()
    except Exception:
        logger.exception('Unhandled exception!')
        sys.exit(1)
