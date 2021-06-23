#!/usr/bin/env python

"""
blog - the greatest static HTML journal generator ever written
"""

import argparse

from lib import files


parser = argparse.ArgumentParser(prog='blog', description=__doc__)


# Globals
parser.add_argument('-v', '--verbose', default=False, action='store_true', help='print debug logs')
parser.add_argument('-s', '--silent', default=False, action='store_true', help='hide all logs')

# subcommands
subparser = parser.add_subparsers(dest='command', required=True, help='command')
build_parser = subparser.add_parser('build', help='build the website')
write_parser = subparser.add_parser('write', help='run website locally in writing mode')
write_parser = subparser.add_parser('help', help='print documentation')
write_parser = subparser.add_parser('version', help='print version and exit')


def main():
    args = parser.parse_args()

    if args.command == 'version':
        with open(files.join('src/VERSION')) as f:
            print(f.read().strip())


if __name__ == '__main__':
    main()
