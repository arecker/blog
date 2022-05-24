import argparse

parser = argparse.ArgumentParser(
    prog='blog', description='the greatest static site generator ever made')

group = parser.add_argument_group('run options')
group.add_argument('--verbose',
                   action='store_true',
                   default=False,
                   help='show debug logs')

group = parser.add_argument_group('directories')
group.add_argument('--dir-data', required=True)
group.add_argument('--dir-entries', required=True)
group.add_argument('--dir-www', required=True)


def parse_args():
    return parser.parse_args()
