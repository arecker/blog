import argparse
import functools
import inspect
import logging
import sys

from .debug import set_trace
from .logger import logger as l
from .version import version as version_string, python_version, python_executable

parser = argparse.ArgumentParser(prog='blog', description='blog - the greatest static HTML journal generator in the world')
parser.add_argument('-d', '--debug', default=False, action='store_true', help='step through code interactively')
parser.add_argument('-s', '--silent', default=False, action='store_true', help='hide all logs')
parser.add_argument('-v', '--verbose', default=False, action='store_true', help='print debug logs')

subparser = parser.add_subparsers(dest='command', help='command')
commands = {}


def command(func):
    functools.wraps(func)
    commands[func.__name__] = func


def register():
    """
    register all the decorated functions with argparse
    """

    for key in sorted(commands.keys()):
        func = commands[key]
        spec = inspect.getargspec(func)
        parser = subparser.add_parser(func.__name__, help=func.__doc__.strip())
        for arg in spec.args:
            parser.add_argument(arg)


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
    l.info(
        'running v%s, python v%s (%s)',
        version_string, python_version, python_executable
    )


def main():
    register()

    arguments = parser.parse_args()

    if arguments.debug:
        info('debug mode enabled, starting trace')
        set_trace()

    if arguments.silent and arguments.verbose:
        error('hey smartass, how am I supposed to be silent AND verbose?')
        sys.exit(1)

    if arguments.silent:
        l.disabled = True
    elif arguments.verbose:
        l.setLevel(logging.DEBUG)
        l.debug('enabled debug logs for --verbose flag')

    func = commands[arguments.command or 'help']
    spec = inspect.getargspec(func)
    psargs = [getattr(arguments, key) for key in spec.args]

    # Finally, we call ther damn thing.
    func(*psargs)
