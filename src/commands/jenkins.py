'''
run the full jenkins pipeline
'''

import logging
import sys

from src import Site

logger = logging.getLogger(__name__)


def register(subparser):
    subparser.add_argument('--netlify-token',
                           required=True,
                           help='Netlify API token')


def main(args):
    site = Site(args)
    logger.info('building site')
    site.build()

    logger.info('deploying site')
    site.deploy()

    if not site.is_entry_tagged:
        logger.info('build finished, since HEAD is not a tagged entry.')
        sys.exit(0)
