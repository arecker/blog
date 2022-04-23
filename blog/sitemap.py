import collections
import datetime
import urllib.parse

SitemapLocation = collections.namedtuple('SitemapLocation', [
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
            location = SitemapLocation(url=url,
                                       lastmod=lastmod,
                                       source=entry.source)
            locations.append(location)
        self.entries = locations

    def locations(self):
        pages = self.entries
        return sorted(pages, key=lambda l: l.url)


def new_sitemap(full_url='', entries=[]):
    sm = Sitemap(full_url)
    sm.add_entries(entries)
    return sm
