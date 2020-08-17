import argparse
import sys


parser = argparse.ArgumentParser(
    prog='blog',
    description='The greatest static site generator ever made',
)

parser.add_argument(
    '-v', '--verbose',
    action='store_true',
    default=False,
    help='show debug logs'
)

parser.add_argument(
    '-s', '--silent',
    action='store_true',
    default=False,
    help='supress all output'
)


def parse_options(args=[]):
    result =  parser.parse_args(args)
    return result
