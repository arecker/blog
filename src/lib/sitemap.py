import collections
import datetime
import logging
import pathlib
import urllib.parse

from .renderer import Renderer

logger = logging.getLogger(__name__)


def render_sitemap(full_url: str, entries=[], pages=[]):
    r = Renderer()

    Location = collections.namedtuple('Location', ['url', 'lastmod'])

    locations = []

    for entry in entries:
        url = urllib.parse.urljoin(full_url, entry.filename)
        lastmod = entry.date
        lastmod = lastmod.replace(tzinfo=datetime.timezone.utc)
        lastmod = lastmod.isoformat()
        locations.append(Location(url=url, lastmod=lastmod))

    for page in pages:
        url = urllib.parse.urljoin(full_url, page)
        locations.append(Location(url=url, lastmod=None))

    feed_attrs = {
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

    with r.wrapping_block('urlset', **feed_attrs):
        for location in sorted(locations, key=lambda l: l.url):
            with r.wrapping_block('url'):
                r.block('loc', contents=location.url)
                if location.lastmod:
                    r.block('lastmod', contents=location.lastmod)

    return r.as_xml(), len(locations)


def write_sitemap(www_dir, full_url, entries=[], pages=[]):
    target = pathlib.Path(www_dir) / 'sitemap.xml'
    rendered, count = render_sitemap(full_url, entries=entries, pages=pages)
    with target.open('w') as f:
        f.write(rendered)
    logging.info('rendered sitemap.xml %d location(s)', count)
