"""blog - the greatest static HTML journal generator ever made"""

import argparse
import collections
import importlib
import logging
import pathlib
import pdb
import pkgutil
import sys
import urllib.parse

from . import __doc__ as DOCSTRING, src_dir, fetch_commands

logger = logging.getLogger(__name__)


def DirectoryType(value, validate=True) -> pathlib.Path:
    directory = pathlib.Path(value).expanduser().absolute()

    if not validate:
        return directory

    if directory.exists() and not directory.is_dir():
        raise argparse.ArgumentTypeError(f'{value} is not a directory!')

    return directory


def URLType(value) -> urllib.parse.ParseResult:
    value = urllib.parse.urlparse(value)
    return value


parser = argparse.ArgumentParser(prog='blog', description=DOCSTRING)
parser.add_argument('-s',
                    '--silent',
                    default=False,
                    action='store_true',
                    help='hide all logs')
parser.add_argument('-v',
                    '--verbose',
                    default=False,
                    action='store_true',
                    help='print debug logs')
parser.add_argument('-d',
                    '--debug',
                    default=False,
                    action='store_true',
                    help='step through code interactively')
parser.add_argument('-o',
                    '--overwrite',
                    default=False,
                    action='store_true',
                    help='Allow pages in webroot to be overwritten')
parser.add_argument('--directory',
                    type=DirectoryType,
                    default=src_dir.parent,
                    help='root directory of website files')
parser.add_argument('--title',
                    type=str,
                    default='Dear Journal',
                    help='website title')
parser.add_argument('--subtitle',
                    type=str,
                    default='Daily, public journal by Alex Recker',
                    help='website subtitle')
parser.add_argument('--author',
                    type=str,
                    default='Alex Recker',
                    help='website author\'s name')
parser.add_argument('--email',
                    type=str,
                    default='alex@reckerfamily.com',
                    help='website author\'s email')
parser.add_argument('--full-url',
                    type=URLType,
                    default='https://www.alexrecker.com',
                    help='Full URL of the website')

# Register subommands from submodules that have a main function.
COMMANDS, subcommand = {}, parser.add_subparsers(dest='subcommand')
for command in fetch_commands():
    COMMANDS[command.name] = command.main_callback
    subparser = subcommand.add_parser(command.name, help=command.doc)
    if command.register_callback:
        # Hand subparser to register function, so the subcommand can
        # add its own arguments
        command.register_callback(subparser)

# Add help subcommand
subcommand.add_parser('help', help='print program usage')


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

    logging.basicConfig(level=level,
                        stream=sys.stderr,
                        format='%(name)s: %(message)s')
    logger.debug('configured logging with level = %s', level)


def main():
    args = parser.parse_args()

    configure_logging(verbose=args.verbose, silent=args.silent)
    logger.debug('parsed args %s, ', vars(args))

    if args.subcommand == 'help':
        parser.print_help()
        sys.exit(0)

    if not args.subcommand:
        parser.print_help()
        sys.exit(1)

    if args.debug:
        logger.info('running %s command interactively for debug mode',
                    args.subcommand)
        pdb.runcall(COMMANDS[args.subcommand], args)
    else:
        logger.debug('invoking main routine of %s', command)
        COMMANDS[args.subcommand](args)


if __name__ == '__main__':
    try:
        main()
    except Exception:
        logger.exception('Unhandled exception!')
        sys.exit(1)
