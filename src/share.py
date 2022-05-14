import argparse
import logging

from . import (tweet, slack)
from .entries import all_entries
from .log import configure_logging

parser = argparse.ArgumentParser()
logger = logging.getLogger(__name__)

parser.add_argument('--dir-data', required=True)
parser.add_argument('--dir-entries', required=True)
parser.add_argument('--slack-channel', default='#blog')
parser.add_argument('--slack-emoji', default=':reckerbot:')
parser.add_argument('--slack-username', default='reckerbot')
parser.add_argument('--slack-webhook-urls', required=True, nargs='+')
parser.add_argument('--twitter-access-token', required=True)
parser.add_argument('--twitter-access-token-secret', required=True)
parser.add_argument('--twitter-consumer-api-key', required=True)
parser.add_argument('--twitter-consumer-api-secret-key', required=True)


def main():
    args = parser.parse_args()
    entries = all_entries(args.dir_entries)
    slack.main(args=args, entries=entries)
    tweet.main(args=args, entries=entries)


if __name__ == '__main__':
    configure_logging()
    main()
