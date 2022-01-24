import argparse
import datetime
import importlib
import logging
import os
import pathlib
import sys
from urllib.parse import urlparse

from . import __doc__ as DOCSTRING

here = pathlib.Path(__file__).parent

logger = logging.getLogger('blog')


def register(parser):
    """Register the commandline parser.

    Place this function in your command file if you wish to add
    additional arguments to the global parser.

    Otherwise you just get this empty function.
    """


class Command:
    def __init__(self, source: pathlib.Path):
        self.source = source

    def __repr__(self):
        return f'<Command {self.name}>'

    @property
    def name(self):
        """Command name, equivalent to commands/<name>.py"""

        return os.path.splitext(self.source.name)[0]

    @property
    def module(self):
        """The command file imported as a module."""

        return importlib.import_module(f'.commands.{self.name}',
                                       package=here.name)

    @property
    def help(self):
        """Pass through to the command file's doc string."""

        return self.module.__doc__.strip()

    @property
    def main(self):
        """Pass through to the command file's main function."""

        try:
            return self.module.main
        except AttributeError:
            raise NotImplementedError(f'{self} has no main function!')

    @property
    def register(self):
        """Pass through to command file's register function.

        Returns an empty one if none is found
        """

        try:
            return self.module.register
        except AttributeError:
            logger.debug(
                '%s has no register function, using empty one instead', self)
            return register


def all_commands():
    files = here.glob('commands/*.py')
    files = [f for f in files if f.name not in ('__init__.py', '__main__.py')]
    files = sorted(files)
    return [Command(source=f) for f in files]


def fetch_command(name: str) -> Command:
    """Fetch command object by name."""

    for command in all_commands():
        if name == command.name:
            return command

    raise ValueError(f'command "{name}" not found!')


def DirectoryType(value, validate=True) -> pathlib.Path:
    """Directory arg type.

    Returns an pathlib object for the provided value, converting it
    into an absolute path and (optionally) validating it along the
    way.

    Use with argparse

    >>> parser = argparse.ArgumentParser()
    >>> _ = parser.add_argument('--directory', type=DirectoryType)
    >>> parser.parse_args(['--directory', '/tmp/']).directory
    PosixPath('/tmp')
    """

    directory = pathlib.Path(value).expanduser().absolute()

    if not validate:
        return directory

    if directory.exists() and not directory.is_dir():
        raise argparse.ArgumentTypeError(f'{value} is not a directory!')

    return directory


def FullURL(value):
    value = urlparse(value)
    return value


def new_command_parser() -> argparse.ArgumentParser:
    """Make a new command parser."""

    parser = argparse.ArgumentParser(prog='blog',
                                     description=DOCSTRING.strip())
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

    parser.add_argument('--title',
                        type=str,
                        default='Dear Journal',
                        help='website title')
    parser.add_argument('--subtitle',
                        type=str,
                        default='Daily, public journal by Alex Recker',
                        help='website subtitle')
    parser.add_argument('--year',
                        type=int,
                        default=datetime.datetime.now().year,
                        help='website copyright year')
    parser.add_argument('--author',
                        type=str,
                        default='Alex Recker',
                        help='website author\'s name')
    parser.add_argument('--email',
                        type=str,
                        default='alex@reckerfamily.com',
                        help='website author\'s email')
    parser.add_argument('--full-url',
                        type=FullURL,
                        default='https://www.alexrecker.com',
                        help='Full URL of the website')
    parser.add_argument('--basepath',
                        type=str,
                        default='/',
                        help='website base path')

    subcommand = parser.add_subparsers(dest='subcommand')
    for command in all_commands():
        subparser = subcommand.add_parser(command.name, help=command.help)
        command.register(subparser)
        logger.debug('registered %s as subcommand', command)

    subcommand.add_parser('help', help='print program usage')

    return parser


def load_command() -> (Command, argparse.ArgumentParser):
    """Load the current command from the system args.

    Will exit and print help documentation if argparse isn't happy.

    Returns Command object as well as parsed args.
    """

    parser = new_command_parser()
    args = parser.parse_args()

    if args.subcommand == 'help':
        parser.print_help()
        sys.exit(0)

    if not args.subcommand:
        parser.print_help()
        sys.exit(1)

    command = fetch_command(args.subcommand)

    return command, args
