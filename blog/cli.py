import argparse
import logging

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(
    prog='blog', description='the greatest static site generator ever made')

parser.add_argument('-v',
                    '--verbose',
                    action='store_true',
                    help='show debug logs')


def parse_args(args):
    result = parser.parse_args(args)
    logger.debug('parsed %s into %s', args, result)
    return result
