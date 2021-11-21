'''
run the full jenkins pipeline
'''

import logging
import sys

from src.commands import test, deploy, slack, tweet
from src.models import Site

logger = logging.getLogger(__name__)


def register(subparser):
    deploy.register(subparser)
    slack.register(subparser)
    tweet.register(subparser)


def main(args):
    test.main(args)
    deploy.main(args)

    if not Site(args).is_entry_tagged:
        sys.exit(0)

    slack.main(args=args)
    tweet.main(args=args)
