"""generate journal RSS feed """
import itertools
import logging

from blog import xml
from blog.models import Page, Site

logger = logging.getLogger(__name__)


class Feed(Page):
    filename = 'feed.xml'

    def __init__(self, site, max_feed_items=30):
        self.site = site
        self.max_feed_items = max_feed_items

    def render(self):
        feed = xml.new_feed(title=self.site.title,
                            subtitle=self.site.subtitle,
                            author=self.site.author,
                            email=self.site.email,
                            timestamp=self.site.latest.date,
                            feed_uri=self.site.href('feed.xml', full=True),
                            site_uri=self.site.href(full=True))

        for item in self.items():
            feed.append(item)

        return xml.stringify_xml(feed)

    def items(self):
        if self.max_feed_items == 0:
            items = self.site.entries
        else:
            items = itertools.islice(self.site.entries, self.max_feed_items)

        return map(xml.as_feed_entry, items)


def register(parser):
    parser.add_argument('--max-feed-items',
                        help='max number of items in RSS feed (0 for none)',
                        type=int,
                        default=30)


def main(args):
    site = Site(**vars(args))
    feed = Feed(site=site, max_feed_items=args.max_feed_items)
    feed.build()
    logger.info('generated RSS feed %s (%d items)', feed,
                len(list(feed.items())))
