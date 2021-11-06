'''
run the full jenkins pipeline
'''

import logging
import sys

from src import Site

logger = logging.getLogger(__name__)


def main(args):
    site = Site(args)
    logger.info('building site')
    site.build()

    if not site.is_entry_tagged:
        logger.info('build finished, since HEAD is not a tagged entry.')
        sys.exit(0)
