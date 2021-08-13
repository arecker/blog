'''
blog - the greatest static HTML journal generator ever made
'''

import argparse
import importlib
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


def register_commands(parser):
    subparser = parser.add_subparsers(dest='subcommand')

    callbacks = {}
    commands = [
        os.path.splitext(p.name)[0]
        for p in root_directory.glob('src/commands/*.py')
        if p.name != '__init__.py'
    ]

    for command in sorted(commands):
        module = importlib.import_module(f'src.commands.{command}')
        subparser.add_parser(command, help=module.__doc__.strip())
        callbacks[command] = module.main

    subparser.add_parser('help', help='print program usage')

    return callbacks


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

    fmt = 'blog - %(levelname)s - %(name)s - %(message)s'

    logging.basicConfig(level=level, stream=sys.stderr, format=fmt)
    logger.debug('configured logging with level = %s', level)


def main():
    callbacks = register_commands(parser)
    args = parser.parse_args()
    configure_logging(verbose=args.verbose, silent=args.silent)
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
