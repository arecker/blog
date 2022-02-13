"""generate sitemap.xml"""

import collections
import logging
import urllib.parse

from . import utils

logger = logging.getLogger(__name__)
Location = collections.namedtuple('Location', ['filename', 'modified'])


def to_xml(location: Location, full_url: urllib.parse.ParseResult) -> str:
    """Convert a Location to XML"""

    item = urllib.parse.urljoin(full_url.geturl(), location.filename)
    item = f'    <loc>{item}</loc>'
    if location.modified:
        item += f'\n    <lastmod>{utils.to_iso_date(location.modified)}</lastmod>'
    return f'  <url>\n{item}\n  </url>\n'


def main(args, entries=[]):
    locations = []

    # index page
    locations.append(Location(modified=None, filename='index.html'))

    # other pages
    locations += [
        Location(modified=None, filename=s)
        for s in ['pets.html', 'contact.html']
    ]

    # entries
    entries = entries or utils.fetch_entries(args.directory / 'entries')
    locations += [
        Location(modified=e.date, filename=e.filename) for e in entries
    ]

    # archives
    locations.append(Location(modified=None, filename='entries.html'))
    years = set([e.date.year for e in entries])
    locations += [Location(modified=None, filename=f'{y}.html') for y in years]

    # convert to XML
    locations = [to_xml(l, full_url=args.full_url) for l in locations]

    # write the sitemap file
    with open(args.directory / 'www/sitemap.xml', 'w') as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>\n')
        f.write(
            '<urlset xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd" xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        )
        f.writelines(locations)
        f.write('</urlset>\n')

    logger.info('generated sitemap.xml with %d location(s)', len(locations))
