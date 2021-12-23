from blog import xml
from blog.models.page import Page

import itertools


class Feed(Page):
    filename = 'feed.xml'

    def __init__(self, site):
        self.site = site

    def render(self):
        feed = xml.new_feed(title=self.site.title,
                            subtitle=self.site.subtitle,
                            author=self.site.author,
                            email=self.site.email,
                            timestamp=self.site.latest.date,
                            feed_uri=self.site.href('feed.xml', full=True),
                            site_uri=self.site.href(full=True))

        for item in self.items():
            feed.append(item)

        return xml.stringify_xml(feed)

    def items(self):
        return map(xml.as_feed_entry, itertools.islice(self.site.entries, 30))
