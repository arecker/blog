'''
run the full jenkins pipeline
'''

import logging
import sys

from blog.commands import test, deploy, slack, tweet
from blog.models import Site

logger = logging.getLogger(__name__)


def register(subparser):
    deploy.register(subparser)
    slack.register(subparser)
    tweet.register(subparser)


def main(args):
    test.main(args)
    deploy.main(args)

    if not Site(**vars(args)).is_entry_tagged:
        sys.exit(0)

    slack.main(args=args)
    tweet.main(args=args)
