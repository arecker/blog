import argparse
import os
import pathlib


def real_file_path(path: str):
    if not os.path.exists(path):
        raise argparse.ArgumentTypeError(f'path {path} does not exist!')

    if not os.path.isfile(path):
        raise argparse.ArgumentTypeError(
            f'path {path} exists, but it\'s not a file!')

    if not os.access(path, os.R_OK):
        raise argparse.ArgumentTypeError(
            f'file {path} exists, but it\'s not readable!')

    return pathlib.Path(path)


def build_subparsers(parser):
    subcommand = parser.add_subparsers(dest='subcommand',
                                       help='subcommand to run')

    # help
    subcommand.add_parser('help', help='print program usage')

    # build
    subparser = subcommand.add_parser('build', help='build the website')

    # render
    subparser = subcommand.add_parser('render',
                                      help='print a rendered page or entry')
    subparser.add_argument('source',
                           type=real_file_path,
                           help='path to source file')

    # serve
    subcommand.add_parser('serve', help='serve the website locally')

    return parser


def build_argparser(default_config_path: str):
    description = 'blog - the greatest static HTML journal generator ever made'
    parser = argparse.ArgumentParser(prog='blog', description=description)

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

    parser.add_argument('-c',
                        '--config',
                        type=real_file_path,
                        default=default_config_path,
                        help='path to config file')

    return build_subparsers(parser)
