import argparse

parser = argparse.ArgumentParser(prog='python -m src')

group = parser.add_argument_group('run options')
group.add_argument('--verbose',
                   action='store_true',
                   default=False,
                   help='show debug logs')
group.add_argument('--dry',
                   action='store_true',
                   default=False,
                   help='don\'t really make changes')

group = parser.add_argument_group('resource directories')
group.add_argument('--dir-data', required=True)
group.add_argument('--dir-entries', required=True)
group.add_argument('--dir-secrets', default=None)
group.add_argument('--dir-www', required=True)

group = parser.add_argument_group('one-off subcommands (exit immediately)')
group.add_argument('--hook',
                   action='store_true',
                   default=False,
                   help='run git pre-commit hook')
group.add_argument('--fixup',
                   action='store_true',
                   default=False,
                   help='tidy up entries and images')
group.add_argument('--slack',
                   action='store_true',
                   default=False,
                   help='share latest entry via slack')
group.add_argument('--tweet',
                   action='store_true',
                   default=False,
                   help='share latest entry via tweet')

group = parser.add_argument_group('additional actions (before/after build)')
group.add_argument('--deploy',
                   action='store_true',
                   default=False,
                   help='deploy the site')
group.add_argument('--share',
                   action='store_true',
                   default=False,
                   help='share new post on social media')


def parse_args():
    return parser.parse_args()
