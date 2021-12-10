"""Functions and objects for parsing main program subcommands and arguments"""

import argparse
import os
import pathlib
import importlib

import src


def get_this_root_directory(this_file=__file__) -> pathlib.Path:
    """Get the root directory of this project

    >>> root = get_this_root_directory()
    >>> root.exists() and root.is_dir()
    True
    """

    this_file = pathlib.Path(this_file)
    return this_file.parent.parent


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


def make_new_parser():
    """Make a new main arg parser.

    >>> parser = make_new_parser()
    >>> values = parser.parse_args(['-dv', 'build'])
    >>> values.debug
    True
    >>> values.verbose
    True
    >>> values.silent
    False
    >>> values.subcommand
    'build'
    """

    parser = argparse.ArgumentParser(prog='blog',
                                     description=src.__doc__.strip())
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

    parser.add_argument('--directory',
                        type=DirectoryType,
                        default=str(get_this_root_directory()),
                        help='path to blog root directory')

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
    parser.add_argument('--domain',
                        type=str,
                        default='www.alexrecker.com',
                        help='website domain')
    parser.add_argument('--protocol',
                        type=str,
                        default='https',
                        help='website protocol')
    parser.add_argument('--basepath',
                        type=str,
                        default='/',
                        help='website base path')

    register_commands(parser)
    return parser


def register_commands(parser):
    """Register all modules in the commands package as program subcommands.

    If the command module has a register() function, call it with the
    subcommand's parser.
    """

    subcommand = parser.add_subparsers(dest='subcommand')

    for command in list_commands():
        module = importlib.import_module(f'src.commands.{command}')
        subparser = subcommand.add_parser(command, help=module.__doc__.strip())

        try:
            module.register(subparser)
        except AttributeError:
            pass

    subcommand.add_parser('help', help='print program usage')


def list_commands(root_directory=get_this_root_directory()):
    """List all the available command names from the command package."""

    return sorted([
        os.path.splitext(p.name)[0]
        for p in root_directory.glob('src/commands/*.py')
        if p.name != '__init__.py'
    ])


def fetch_callback_for_command(command):
    """Fetch a command by name as a callable."""

    module = importlib.import_module(f'src.commands.{command}')
    return module.main
