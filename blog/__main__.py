'''
blog - the greatest static HTML journal generator ever made
'''

import logging
import pdb
import sys

from blog.args import (make_new_parser, fetch_callback_for_command)

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

    fmt = '[%(levelname)s] %(message)s'
    logging.basicConfig(level=level, stream=sys.stderr, format=fmt)
    logger.debug('configured logging with level = %s', level)


def main():
    parser = make_new_parser()
    args = parser.parse_args()
    configure_logging(verbose=args.verbose, silent=args.silent)
    logger.debug('parsed args %s, ', vars(args))

    if args.subcommand == 'help':
        parser.print_help()
        sys.exit(0)

    if not args.subcommand:
        parser.print_help()
        sys.exit(1)

    callback = fetch_callback_for_command(args.subcommand)

    if args.debug:
        logger.info('running %s command interactively for debug mode',
                    args.subcommand)
        pdb.runcall(callback, args)
    else:
        callback(args)


if __name__ == '__main__':
    try:
        main()
    except Exception:
        logger.exception('Unhandled exception!')
        sys.exit(1)
