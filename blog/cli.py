import argparse
import collections
import datetime
import functools
import logging
import pathlib
import pdb
import platform
import re
import sys
import urllib.parse

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(
    prog='blog', description='The greatest static site generator ever made')

group = parser.add_argument_group('program')
parser.add_argument('-d',
                    '--debug',
                    action='store_true',
                    help='run code in a debugger')
parser.add_argument('-v',
                    '--verbose',
                    action='store_true',
                    help='show debug logs')

home = pathlib.Path.home()
group = parser.add_argument_group('directories')
group.add_argument('--dir-www',
                   default=str(home / 'src/blog/www'),
                   help='output directory')
group.add_argument('--dir-entries',
                   default=str(home / 'src/blog/entries/'),
                   help='entry sources directory')

group = parser.add_argument_group('site')
group.add_argument('--site-url',
                   help='full site url',
                   default='https://www.alexrecker.com')
group.add_argument('--site-author',
                   help='copyright author',
                   default='Alex Recker')
group.add_argument('--site-year',
                   help='copyright year',
                   default=datetime.datetime.now().year)

subcommand = parser.add_subparsers(dest='subcommand', metavar='{subcommand}')
subcommand.add_parser('help', help='Print program usage')


def parse_args(args):
    args = parser.parse_args(args)
    args.dir_www = pathlib.Path(args.dir_www)
    args.dir_entries = pathlib.Path(args.dir_entries)
    args.site_url = urllib.parse.urlparse(args.site_url)
    return args


def configure_logging(verbose=False):
    """Configures root logger."""

    logger = logging.getLogger()

    if verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logger.setLevel(level)

    handler = logging.StreamHandler()
    handler.setLevel(level)

    formatter = logging.Formatter('%(name)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


Command = collections.namedtuple('Command', [
    'name',
    'docstring',
    'function',
])

COMMANDS = {}


def register_command(func):
    functools.wraps(func)
    cmd = Command(name=func.__name__,
                  docstring=func.__doc__.strip(),
                  function=func)
    COMMANDS[cmd.name] = cmd
    subcommand.add_parser(cmd.name, help=cmd.docstring)
    logger.debug('registered %s', cmd)
    return func


def main(args=sys.argv[1:]):
    args = parse_args(args=args)

    configure_logging(verbose=args.verbose)

    logger.debug(
        'running blog program using python v%s from "%s" with args %s',
        platform.python_version(),
        pathlib.Path.cwd().absolute(), vars(args))

    if args.subcommand == 'help':
        parser.print_help()
        return sys.exit(0)

    if not args.subcommand:
        logger.error('subcommand expected')
        parser.print_help()
        return sys.exit(1)

    command = COMMANDS[args.subcommand]
    if args.debug:
        logger.info('running %s command interactively in a debugger',
                    command.name)
        pdb.runcall(command.function, args)
    else:
        command.function(args)
