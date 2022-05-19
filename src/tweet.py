"""share latest entry in a tweet"""
import argparse
import json
import logging
import pathlib
import sys
import urllib.parse

from .entries import all_entries
from .lib import configure_logging

logger = logging.getLogger(__name__)
parser = argparse.ArgumentParser()

parser.add_argument('--dir-entries', required=True)
parser.add_argument('--dir-data', required=True)
parser.add_argument('--twitter-consumer-api-key', required=True)
parser.add_argument('--twitter-consumer-api-secret-key', required=True)
parser.add_argument('--twitter-access-token', required=True)
parser.add_argument('--twitter-access-token-secret', required=True)


def load_full_url(data_dir):
    with (pathlib.Path(data_dir) / 'info.json').open('r') as f:
        return json.load(f)['url']


def make_twitter_client(args):
    import tweepy
    auth = tweepy.OAuthHandler(args.twitter_consumer_api_key,
                               args.twitter_consumer_api_secret_key)
    auth.set_access_token(args.twitter_access_token,
                          args.twitter_access_token_secret)
    return tweepy.API(auth)


def main(args=None, entries=[]):
    args = args or parser.parse_args()

    full_url = load_full_url(args.dir_data)

    entries = entries or all_entries(args.dir_entries)
    latest = entries[0]

    try:
        client = make_twitter_client(args)
    except ImportError:
        logger.error('tweepy librarly not found, tweet command not available')
        sys.exit(1)

    url = urllib.parse.urljoin(full_url, latest.filename)

    tweet = '\n'.join([latest.title, latest.description, url])
    client.update_status(tweet)
    logger.info('shared "%s" to twitter', latest.description)


if __name__ == '__main__':
    configure_logging()
    main()
