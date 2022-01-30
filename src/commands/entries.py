"""build journal entries"""

import logging
import datetime

from .pages import Page, build_nav_list
from .. import html

logger = logging.getLogger(__name__)


class Entry(Page):
    def __repr__(self):
        return f'<Entry {self.filename}>'

    @property
    def title(self):
        return self.date.strftime('%A, %B %-d %Y')

    @property
    def description(self):
        metadata = self.metadata()
        return metadata['title']

    @property
    def date(self):
        return datetime.datetime.strptime(self.slug, '%Y-%m-%d')

    def paginate(self, next_filename=None, previous_filename=None):
        self.next_filename = next_filename
        self.previous_filename = previous_filename

    def read(self):
        content = super(Entry, self).read()
        pagination = html.build_page_pagination(
            next_page=self.next_filename, previous_page=self.previous_filename)
        pagination = html.stringify_xml(pagination)
        return content + '\n' + pagination


def register(parser):
    return parser


def main(args):
    # TODO: remove once Site is gone
    from ..models import Site
    site = Site(**vars(args))

    total = len(list(site.entries))
    nav_pages = build_nav_list()
    for i, page in enumerate(site.entries):
        page.build(author=args.author,
                   year=args.year,
                   full_url=args.full_url,
                   nav_pages=nav_pages)
        logger.debug('generated %s (%d/%d)', page.target, i + 1, total)
        if (i + 1) % 100 == 0 or (i + 1) == total:
            logger.info('generated %d out of %d entries', i + 1, total)
