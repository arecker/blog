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

    def render(self, author='', email='', title='', subtitle=''):
        if not title:
            raise ValueError('title not set!')
        if not author:
            raise ValueError('author not set!')
        if not email:
            raise ValueError('email not set!')
        if not subtitle:
            raise ValueError('subtitle not set!')

        feed = xml.new_feed(title=title,
                            subtitle=subtitle,
                            author=author,
                            email=email,
                            timestamp=self.site.latest.date,
                            feed_uri=self.site.href('feed.xml', full=True),
                            site_uri=self.site.href(full=True))

        for item in self.items(author=author, email=email):
            feed.append(item)

        return xml.stringify_xml(feed)

    def items(self, author='', email='', **kwargs):
        if self.max_feed_items == 0:
            items = self.site.entries
        else:
            items = itertools.islice(self.site.entries, self.max_feed_items)

        return [
            xml.as_feed_entry(entry, author=author, email=email)
            for entry in items
        ]


def register(parser):
    parser.add_argument('--max-feed-items',
                        help='max number of items in RSS feed (0 for none)',
                        type=int,
                        default=30)


def main(args):
    site = Site(**vars(args))
    feed = Feed(site=site, max_feed_items=args.max_feed_items)
    kwargs = {
        'author': args.author,
        'email': args.email,
        'subtitle': args.subtitle,
        'title': args.title,
    }
    feed.build(**kwargs)
    logger.info('generated RSS feed %s (%d items)', feed,
                len(list(feed.items(**kwargs))))
