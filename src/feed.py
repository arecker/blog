import collections


Feed = collections.namedtuple('Feed', [
    'items',
])
FeedItem = collections.namedtuple('FeedItem', [
])


def new_rss_feed(context) -> FeedItem:
    kwargs = {'items': []}

    return Feed(**kwargs)
