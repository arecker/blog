import argparse
import os


def real_file_path(path: str):
    if not os.path.exists(path):
        raise argparse.ArgumentTypeError(f'path {path} does not exist!')

    if not os.path.isfile(path):
        raise argparse.ArgumentTypeError(
            f'path {path} exists, but it\'s not a file!')

    if not os.access(path, os.R_OK):
        raise argparse.ArgumentTypeError(
            f'file {path} exists, but it\'s not readable!')

    return path


def build_subparsers(parser, subcommands):
    subparser = parser.add_subparsers(dest='subcommand',
                                      help='subcommand to run')

    for key in sorted(subcommands.keys()):
        info = subcommands[key]
        localparser = subparser.add_parser(key, help=info['help'])
        for posarg in info.get('posargs', []):
            localparser.add_argument(
                posarg['key'],
                type=posarg['type'],
                help=posarg['help'],
            )

    return parser


def build_global_argparser(default_config_path: str, subcommands={}):
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

    return build_subparsers(parser, subcommands)
