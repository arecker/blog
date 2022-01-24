"""generate journal RSS feed """
from urllib.parse import urljoin
import itertools
import logging

from blog import xml2 as xml
from blog.models import Page, Site

logger = logging.getLogger(__name__)


class Feed(Page):
    filename = 'feed.xml'

    def __init__(self, site, max_feed_items=30):
        self.site = site
        self.max_feed_items = max_feed_items

    def render(self, author='', email='', title='', subtitle='', full_url=''):
        assert full_url
        feed_url = urljoin(
            f'{full_url.scheme}://{full_url.netloc}{full_url.path}',
            '/feed.xml',
        )
        site_url = f'{full_url.scheme}://{full_url.netloc}{full_url.path}'

        assert all([title, subtitle, author, email])
        feed = xml.new_feed(title=title,
                            subtitle=subtitle,
                            author=author,
                            email=email,
                            timestamp=self.site.latest.date,
                            feed_uri=feed_url,
                            site_uri=site_url)

        for item in self.items(author=author, email=email, full_url=full_url):
            feed.append(item)

        return xml.stringify_xml(feed)

    def items(self, author='', email='', full_url='', **kwargs):
        if self.max_feed_items == 0:
            items = self.site.entries
        else:
            items = itertools.islice(self.site.entries, self.max_feed_items)

        return [
            xml.as_feed_entry(entry,
                              author=author,
                              email=email,
                              full_url=full_url) for entry in items
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
        'full_url': args.full_url
    }
    feed.build(**kwargs)
    logger.info('generated RSS feed %s (%d items)', feed,
                len(list(feed.items(**kwargs))))
