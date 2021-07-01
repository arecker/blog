import argparse
import functools
import logging
import sys

from .version import version as version_string, python_version, python_executable
from .logger import info, error, logger

parser = argparse.ArgumentParser(prog='blog', description='blog - the greatest static HTML journal generator ever written')
parser.add_argument('-v', '--verbose', default=False, action='store_true', help='print debug logs')
parser.add_argument('-s', '--silent', default=False, action='store_true', help='hide all logs')

subparser = parser.add_subparsers(dest='command', help='command')
commands = {}


def command(func):
    functools.wraps(func)
    commands[func.__name__] = func
    subparser.add_parser(func.__name__, help=func.__doc__.strip())


@command
def help():
    """
    print program documentation
    """
    parser.print_help()


@command
def version():
    """
    print program information
    """
    info(f'v{version_string}, python v{python_version} ({python_executable})')


def main():
    args = parser.parse_args()

    if args.silent and args.verbose:
        error('hey smartass, how am I supposed to be silent AND verbose?')
        sys.exit(1)

    if args.silent:
        logger.disabled = True
    elif args.verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug('enabled debug logs for --verbose flag')

    commands[args.command or 'help']()
