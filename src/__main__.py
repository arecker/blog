'''
blog - the greatest static HTML journal generator ever made
'''

import argparse
import importlib
import itertools
import logging
import os
import pathlib
import sys

import src as blog

logger = logging.getLogger(__name__)

this_directory = os.path.dirname(os.path.realpath(__file__))
root_directory = pathlib.Path(
    os.path.abspath(os.path.join(this_directory, '../')))

parser = argparse.ArgumentParser(prog='blog', description=__doc__.strip())
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

parser.add_argument('-r',
                    '--root_directory',
                    type=pathlib.Path,
                    default=root_directory,
                    help='path to blog root directory')

parser.add_argument('-c',
                    '--config',
                    type=pathlib.Path,
                    default=root_directory / 'blog.conf',
                    help='path to config file')

subparser = parser.add_subparsers(dest='subcommand', help='subcommand to run')


def register_commands():
    global parser
    global subparser

    callbacks = {}
    command_files = [p.name for p in root_directory.glob('src/commands/*.py')]
    command_modules = [
        os.path.splitext(p)[0] for p in command_files if p != '__init__.py'
    ]

    for module in command_modules:
        command = importlib.import_module(f'src.commands.{module}')
        subparser.add_parser(module, help=command.__doc__.strip())
        callbacks[module] = command.main

    return callbacks


subparser.add_parser('help', help='print program usage')
callbacks = register_commands()


def main():
    args = parser.parse_args()
    blog.configure_logging(verbose=args.verbose, silent=args.silent)
    logger.debug('parsed args %s, ', vars(args))

    if args.subcommand == 'help':
        parser.print_help()
        sys.exit(0)

    config = blog.load_config(args.config)
    context = blog.build_global_context(root_directory=args.root_directory,
                                        config=config,
                                        file_wrapper=blog.Page)

    try:
        callbacks[args.subcommand](config=config, context=context)
    except KeyError:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    try:
        main()
    except Exception:
        logger.exception('Unhandled exception!')
        sys.exit(1)
