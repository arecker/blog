import itertools

from src import xml
from src.models.page import Page


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
        for page in itertools.chain(self.site.entries, self.site.pages):
            url = self.site.href(page.filename, full=True)
            if page.is_entry:
                yield url, page.date
            else:
                yield url, self.site.timestamp
