"""run the full jenkins pipeline"""

import blog
import logging
import sys

from . import deploy, slack, tweet

logger = logging.getLogger(__name__)


def register(subparser):
    deploy.register(subparser)
    slack.register(subparser)
    tweet.register(subparser)


def main(args):
    deploy.main(args)

    if not blog.git_latest_tag():
        logger.info('exiting, since HEAD commit is not tagged')
        sys.exit(0)

    slack.main(args=args)
    tweet.main(args=args)
