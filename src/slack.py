"""share latest entry in a slack post"""

import argparse
import json
import logging
import pathlib
import urllib.parse

from .entries import all_entries
from .http import make_http_request
from .log import configure_logging

logger = logging.getLogger(__name__)
parser = argparse.ArgumentParser()

parser.add_argument('--dir-entries', required=True)
parser.add_argument('--dir-data', required=True)
parser.add_argument('--slack-webhook-urls', required=True, nargs='+')
parser.add_argument('--slack-channel', default='#blog')
parser.add_argument('--slack-username', default='reckerbot')
parser.add_argument('--slack-emoji', default=':reckerbot:')


def load_full_url(data_dir):
    with (pathlib.Path(data_dir) / 'info.json').open('r') as f:
        return json.load(f)['url']


def main(args=None, entries=[]):
    args = args or parser.parse_args()

    entries = entries or all_entries(args.directory / 'entries')
    latest = entries[0]
    full_url = load_full_url(args.dir_data)
    url = urllib.parse.urljoin(full_url, latest.filename)

    message = '\n'.join([latest.title, latest.description, url])
    payload = {
        'text': message,
        'channel': args.slack_channel,
        'username': args.slack_username,
        'icon_emoji': args.slack_emoji
    }

    for url in args.slack_webhook_urls:
        make_http_request(url=url, method='POST', data=payload)
        logger.info('shared "%s" to slack channel %s', latest.description,
                    args.slack_channel)


if __name__ == '__main__':
    configure_logging()
    main()
