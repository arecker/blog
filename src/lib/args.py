import argparse

parser = argparse.ArgumentParser(prog='python -m src')

group = parser.add_argument_group('run options')
group.add_argument('--verbose',
                   action='store_true',
                   default=False,
                   help='show debug logs')

group = parser.add_argument_group('resource directories')
group.add_argument('--dir-data', required=True)
group.add_argument('--dir-entries', required=True)
group.add_argument('--dir-www', required=True)

group = parser.add_argument_group('one-off subcommands (exit immediately)')
group.add_argument('--fixup',
                   action='store_true',
                   default=False,
                   help='tidy up entries and images')


def parse_args():
    return parser.parse_args()
