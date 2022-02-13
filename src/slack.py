"""share latest entry in a slack post"""

import logging
import urllib.parse

from . import http, utils

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


def main(args, entries=[]):
    entries = entries or utils.fetch_entries(args.directory / 'entries')
    latest = entries[0]
    url = urllib.parse.urljoin(args.full_url.geturl(), latest.filename)

    message = '\n'.join([latest.title, latest.description, url])
    payload = {
        'text': message,
        'channel': args.slack_channel,
        'username': args.slack_username,
        'icon_emoji': args.slack_emoji
    }

    for url in args.slack_webhook_urls:
        http.make_request(url=url, method='POST', data=payload)
        logger.info('shared "%s" to slack channel %s', latest.description,
                    args.slack_channel)
