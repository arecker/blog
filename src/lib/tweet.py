"""share latest entry in a tweet"""
import collections
import json
import logging
import pathlib
import sys
import urllib.parse

logger = logging.getLogger(__name__)

Credentials = collections.namedtuple('Credentials', [
    'access_token',
    'access_token_secret',
    'consumer_api_key',
    'consumer_api_secret_key',
])


def make_twitter_client(creds):
    import tweepy
    auth = tweepy.OAuthHandler(creds.consumer_api_key,
                               creds.consumer_api_secret_key)
    auth.set_access_token(creds.access_token, creds.access_token_secret)
    return tweepy.API(auth)


def share_latest_as_tweet(latest=None,
                          full_url=None,
                          creds_dir=None,
                          dry=False):
    try:
        with (pathlib.Path(creds_dir) / 'twitter.json').open('r') as f:
            data = json.load(f)
            creds = Credentials(**data)
            client = make_twitter_client(creds)
    except ImportError:
        logger.error('tweepy library not found, tweet command not available')
        sys.exit(1)

    url = urllib.parse.urljoin(full_url, latest.filename)

    tweet = '\n'.join([latest.title, latest.description, url])
    if dry:
        logger.warn('running in dry mode, but would have tweeted this:\n%s',
                    tweet)
    else:
        client.update_status(tweet)
    logger.info('shared "%s" to twitter', latest.description)


if __name__ == '__main__':
    lib.configure_logging()
    main()
