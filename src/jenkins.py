"""run the full jenkins pipeline"""

import logging
import sys

from . import deploy, slack, tweet, git, test

logger = logging.getLogger(__name__)


def register(subparser):
    deploy.register(subparser)
    slack.register(subparser)
    tweet.register(subparser)


def main(args):
    test.main(args)
    deploy.main(args)

    if not git.head_is_entry_tagged(args.directory):
        logger.info('exiting, since HEAD commit is not tagged')
        sys.exit(0)

    slack.main(args=args)
    tweet.main(args=args)
