'''
run the full jenkins pipeline
'''

import logging
import sys

from src import Site
from src.commands import test, deploy

logger = logging.getLogger(__name__)


def register(subparser):
    subparser.add_argument('--netlify-token',
                           required=True,
                           help='Netlify API token')


def main(args):
    test.main(args)
    deploy.main(args)

    if not Site(args).is_entry_tagged:
        sys.exit(0)
