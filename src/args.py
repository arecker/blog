import argparse
import os
import pathlib

this_directory = os.path.dirname(os.path.realpath(__file__))
root_directory = pathlib.Path(
    os.path.abspath(os.path.join(this_directory, '../')))


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


def real_directory_path(path: str):
    if not os.path.exists(path):
        raise argparse.ArgumentTypeError(f'path {path} does not exist!')

    if not os.path.isdir(path):
        raise argparse.ArgumentTypeError(
            f'path {path} exists, but it\'s not a directory!')

    return pathlib.Path(path)


def build_subparsers(parser):
    subcommand = parser.add_subparsers(dest='subcommand',
                                       help='subcommand to run')

    # help
    subcommand.add_parser('help', help='print program usage')

    # build
    subparser = subcommand.add_parser('build', help='build the website')

    # images
    subcommand.add_parser('images', help='resize images')

    # jenkins
    subcommand.add_parser('jenkins', help='run built-in jenkins pipeline')

    # publish
    subcommand.add_parser('publish', help='publish working files as new entry')

    # render
    subparser = subcommand.add_parser('render',
                                      help='print a rendered page or entry')
    subparser.add_argument('source',
                           type=real_file_path,
                           help='path to source file')

    # serve
    subcommand.add_parser('serve', help='serve the website locally')

    return parser


def build_argparser():
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

    parser.add_argument('-r',
                        '--root_directory',
                        type=real_directory_path,
                        default=root_directory,
                        help='path to blog root directory')

    parser.add_argument('-c',
                        '--config',
                        type=real_file_path,
                        default=root_directory / 'blog.conf',
                        help='path to config file')

    return build_subparsers(parser)
