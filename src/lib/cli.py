import argparse
import functools

from . import files

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
    shows help documentation
    """
    parser.print_help()


@command
def version():
    """
    show version and exit
    """
    with open(files.join('src/VERSION')) as f:
        print(f.read().strip())


def main():
    args = parser.parse_args()
    commands[args.command or 'help']()
