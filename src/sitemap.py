import collections
import datetime
import logging
import pathlib
import urllib.parse

from .renderer import Renderer

logger = logging.getLogger(__name__)

Location = collections.namedtuple('Location', [
    'url',
    'lastmod',
    'source',
])


class Sitemap:
    def __init__(self, full_url):
        self.entries = []
        if isinstance(full_url, str):
            full_url = urllib.parse.urlparse(full_url)
        self.full_url = full_url

    def __len__(self):
        return len(self.locations())

    def add_entries(self, entries):
        locations = []
        for entry in entries:
            url = urllib.parse.urljoin(self.full_url.geturl(), entry.filename)
            lastmod = entry.date
            lastmod = lastmod.replace(tzinfo=datetime.timezone.utc)
            lastmod = lastmod.isoformat()
            location = Location(url=url, lastmod=lastmod, source=entry.source)
            locations.append(location)
        self.entries = locations

    def locations(self):
        pages = self.entries
        return sorted(pages, key=lambda l: l.url)


def new_sitemap(full_url='', entries=[]):
    sm = Sitemap(full_url)
    sm.add_entries(entries)
    return sm


def render_sitemap(sm: Sitemap):
    r = Renderer()
    urlset_attrs = {
        'xmlns:xsi':
        'http://www.w3.org/2001/XMLSchema-instance',
        'xsi:schemaLocation':
        ' '.join([
            'http://www.sitemaps.org/schemas/sitemap/0.9',
            'http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd'
        ]),
        'xmlns':
        'http://www.sitemaps.org/schemas/sitemap/0.9'
    }

    locations = sm.locations()
    with r.wrapping_block('urlset', **urlset_attrs):
        for location in locations:
            with r.wrapping_block('url'):
                r.block('loc', contents=location.url)
                if location.lastmod:
                    r.block('lastmod', contents=location.lastmod)

    return r.as_xml()


def write_sitemap(www_dir, full_url='', entries=[]):
    sm = new_sitemap(full_url=full_url, entries=entries)
    target = pathlib.Path(www_dir) / 'sitemap.xml'
    with target.open('w') as f:
        f.write(render_sitemap(sm))
    logger.info('wrote sitemap.xml with %d location(s)', len(sm))
