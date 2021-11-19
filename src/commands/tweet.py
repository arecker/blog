"""share latest entry in a tweet"""

import logging
import sys

from src import Site

logger = logging.getLogger(__name__)


def register(subparser):
    subparser.add_argument('--twitter-consumer-api-key', required=True)
    subparser.add_argument('--twitter-consumer-api-secret-key', required=True)
    subparser.add_argument('--twitter-access-token', required=True)
    subparser.add_argument('--twitter-access-token-secret', required=True)


def make_twitter_client(args):
    import tweepy
    auth = tweepy.OAuthHandler(args.twitter_consumer_api_key,
                               args.twitter_consumer_api_secret_key)
    auth.set_access_token(args.twitter_access_token,
                          args.twitter_access_token_secret)
    return tweepy.API(auth)


def main(args):
    try:
        client = make_twitter_client(args)
    except ImportError:
        logger.error('tweepy librarly not found, tweet command not available')
        sys.exit(1)

    site = Site(args=args)
    url = site.uri + site.latest.filename
    tweet = '\n'.join([site.latest.title, site.latest.description, url])
    client.update_status(tweet)
    logger.info('shared "%s" to twitter', site.latest.description)
