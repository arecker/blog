"""share latest entry in a slack post"""

import logging

from blog import http
from blog.models import Site

logger = logging.getLogger(__name__)


def register(subparser):
    subparser.add_argument('--slack-webhook-urls',
                           required=True,
                           nargs='+',
                           help='slack incoming webhook URLs')
    subparser.add_argument('--slack-channel',
                           default='#blog',
                           help='slack channel')
    subparser.add_argument('--slack-username',
                           default='reckerbot',
                           help='slack bot username')
    subparser.add_argument('--slack-emoji',
                           default=':reckerbot:',
                           help='slack bot icon')


def main(args):
    site = Site(**vars(args))
    url = site.latest.href(full=True)
    message = '\n'.join([site.latest.title, site.latest.description, url])
    payload = {
        'text': message,
        'channel': args.slack_channel,
        'username': args.slack_username,
        'icon_emoji': args.slack_emoji
    }

    for url in args.slack_webhook_urls:
        http.make_request(url=url, method='POST', data=payload)
        logger.info('shared "%s" to slack channel %s', site.latest.description,
                    args.slack_channel)