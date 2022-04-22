import argparse
import collections
import functools
import logging
import pathlib
import pathlib
import pdb
import platform
import re
import sys

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(
    prog='blog', description='The greatest static site generator ever made')

parser.add_argument('-v',
                    '--verbose',
                    action='store_true',
                    help='show debug logs')
parser.add_argument('-d',
                    '--debug',
                    action='store_true',
                    help='run code in a debugger')

subcommand = parser.add_subparsers(dest='subcommand', metavar='{subcommand}')
subcommand.add_parser('help', help='Print program usage')


def parse_args(args):
    result = parser.parse_args(args)
    return result


class LogFormatter(logging.Formatter):

    def format(self, *args, **kwargs):
        result = super().format(*args, **kwargs)
        return prettify_log(result)


def prettify_log(message: str):
    """Prettify a log message."""

    message = re.sub(f'{pathlib.Path.home()}', '~', message)
    return message


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

    formatter = LogFormatter('[%(levelname)s] %(message)s')
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
