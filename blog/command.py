import argparse
import functools
import inspect
import logging
import pdb
import sys

from . import logger

# All registered commands are stored here.
#
# '<subcommand>': func
commands = {}


def register_command(func):
    """Register a function as a top level command

    >>> test_function = lambda: print('decorate me!')
    >>> command_function = register_command(test_function)
    """

    functools.wraps(func)
    commands[func.__name__] = func
    return func


def build_arg_parser():
    """Convert registered commands into an arg parser

    >>> parser = build_arg_parser()
    >>> parser.prog
    'blog'
    """

    parser = argparse.ArgumentParser(
        prog='blog',
        description=
        'blog - the greatest static HTML journal generator ever made')

    # Add global flags
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

    subparser = parser.add_subparsers(dest='command', help='command')

    # Default help function
    @register_command
    def help():
        """print program usage"""
        parser.print_help()

    # Add subparsers for each registered command
    for key in sorted(commands.keys()):
        func = commands[key]
        args = inspect.signature(func).parameters
        note = func.__doc__.strip()
        this_parser = subparser.add_parser(key, help=note)
        for arg in args:
            this_parser.add_argument(arg)

        logger.debug('registered command %s with args %s', key, args)

    return parser


def extract_subargs(args: dict, function: callable):
    """Pull list from args based on signature of function

    >>> function = lambda a, b: a + 1
    >>> args = {'a': 1, 'b': 2, 'c': 3}
    >>> extract_subargs(args, function)
    [1, 2]
    """

    subargs = []

    for param in inspect.signature(function).parameters:
        subargs.append(args.get(param))

    return subargs


def main():
    """Main routine.

    Registers commands, parses args, interacts with global options,
    then finally runs the appropriate registered command.
    """

    parser = build_arg_parser()
    args = parser.parse_args()

    if args.silent and args.verbose:
        raise RuntimeError(
            'hey smartass, how am I supposed to be silent AND verbose?')

    if args.silent:
        logger.disabled = True
    elif args.verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug('enabled debug logs for --verbose flag')

    try:
        function = commands[args.command]
    except KeyError:
        if not args.command:
            logger.error('command required')
        else:
            logger.error('invalid command "%s"', args.command)

        parser.print_help()
        sys.exit(1)

    subargs = extract_subargs(vars(args), function)
    logger.debug('calling %s with args %s', function, subargs)

    if args.debug:
        logger.info('enabling interactive trace for --debug flag')
        pdb.runcall(function, *subargs)
    else:
        function(*subargs)
