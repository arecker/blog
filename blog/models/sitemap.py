import itertools

from blog import xml
from blog.models.page import Page


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
                                self.site.archive.pages())
        for page in pages:
            url = self.site.href(page.filename, full=True)
            if page.is_entry:
                yield url, page.date
            else:
                yield url, self.site.timestamp
