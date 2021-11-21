import itertools
import datetime
from xml.etree import ElementTree as ET


class Sitemap:
    def __init__(self, site):
        self.site = site

    def __repr__(self):
        return '<Sitemap sitemap.xml>'

    @property
    def target(self):
        return 'www/sitemap.xml'

    def to_iso_date(self, date):
        return date.replace(tzinfo=datetime.timezone.utc).isoformat()

    def render(self):
        sitemap = ET.Element('urlset', attrib=self.attributes())

        for location in self.locations():
            sitemap.append(location)

        ET.indent(sitemap)
        xml = ET.tostring(sitemap, encoding='unicode', method='xml')
        return f'<?xml version="1.0" encoding="utf-8"?>\n{xml}'

    def build(self):
        with open(self.site.directory / 'www/sitemap.xml', 'w') as f:
            f.write(self.render())

    def attributes(self):
        return {
            'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
            'xsi:schemaLocation':
            'http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd',
            'xmlns': 'http://www.sitemaps.org/schemas/sitemap/0.9'
        }

    def locations(self):
        for page in itertools.chain(self.site.entries, self.site.pages):
            url = ET.TreeBuilder()
            url.start('url', {})
            url.start('loc', {})
            url.data(self.site.href(page.filename))
            url.end('loc')

            if page.is_entry:
                url.start('lastmod', {})
                url.data(self.to_iso_date(page.date))
                url.end('lastmod')

            url.end('url')

            yield url.close()
