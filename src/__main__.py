'''
blog - the greatest static HTML journal generator ever made
'''

import logging
import pdb
import sys

from . import load_command

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

    logging.basicConfig(level=level, stream=sys.stderr)
    logger.debug('configured logging with level = %s', level)


def main():
    command, args = load_command()

    configure_logging(verbose=args.verbose, silent=args.silent)
    logger.debug('parsed args %s, ', vars(args))

    if args.debug:
        logger.info('running %s command interactively for debug mode',
                    args.subcommand)
        pdb.runcall(command.main, args)
    else:
        logger.debug('invoking main routine of %s', command)
        command.main(args)


if __name__ == '__main__':
    try:
        main()
    except Exception:
        logger.exception('Unhandled exception!')
        sys.exit(1)
