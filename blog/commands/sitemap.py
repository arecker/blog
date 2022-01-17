"""generate sitemap.xml"""
import itertools
import logging

from blog import xml
from blog.commands.archives import Archive
from blog.models import Page, Site

logger = logging.getLogger(__name__)


class Sitemap(Page):
    filename = 'sitemap.xml'

    def __init__(self, site):
        self.site = site

    def render(self):
        root = xml.new_sitemap()

        for element in xml.as_location_elements(locations=self.locations):
            root.append(element)

        return xml.stringify_xml(root)

    @property
    def locations(self):
        pages = itertools.chain(self.site.entries, self.site.pages,
                                Archive(site=self.site).pages())
        pages = sorted(pages, key=lambda p: p.filename)
        for page in pages:
            url = self.site.href(page.filename, full=True)
            if page.is_entry:
                yield url, page.date
            else:
                yield url, self.site.timestamp


def main(args):
    site = Site(**vars(args))
    sitemap = Sitemap(site=site)
    sitemap.build()
    logger.info('generated sitemap %s (%d locations)', sitemap,
                len(list(sitemap.locations)))
