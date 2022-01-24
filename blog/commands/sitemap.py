"""generate sitemap.xml"""
import itertools
import logging
from urllib.parse import urljoin

from blog import xml
from blog.commands.archives import Archive
from blog.models import Page, Site

logger = logging.getLogger(__name__)


class Sitemap(Page):
    filename = 'sitemap.xml'

    def __init__(self, site, full_url):
        self.site = site
        self.full_url = full_url

    def render(self):
        root = xml.new_sitemap()

        for element in xml.as_location_elements(locations=self.locations):
            root.append(element)

        return xml.stringify_xml(root)

    def href(self, path):
        url = self.full_url.scheme
        url += '://' + self.full_url.netloc
        url += self.full_url.path
        return urljoin(url, path)

    @property
    def locations(self):
        pages = itertools.chain(
            self.site.entries, self.site.pages,
            Archive(site=self.site, full_url=self.full_url).pages())
        pages = sorted(pages, key=lambda p: p.filename)
        for page in pages:
            url = self.href(page.filename)
            if page.is_entry:
                yield url, page.date
            else:
                yield url, self.site.timestamp


def main(args):
    site = Site(**vars(args))
    sitemap = Sitemap(site=site, full_url=args.full_url)
    sitemap.build()
    logger.info('generated sitemap %s (%d locations)', sitemap,
                len(list(sitemap.locations)))
