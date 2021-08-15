import datetime
import itertools
import logging

from xml.etree import ElementTree as ET

logger = logging.getLogger(__name__)


class Feed(object):
    def __init__(self, site):
        self.site = site

    def __repr__(self):
        return '<Feed feed.xml>'

    @property
    def target(self):
        return 'www/feed.xml'

    def render(self):
        feed = ET.Element('feed', xmlns='http://www.w3.org/2005/Atom')
        feed.append(self.title())
        feed.append(self.subtitle())
        feed.append(self.author())
        feed.append(self.updated())
        for element in self.links():
            feed.append(element)
        feed.append(self.identifier())
        for item in self.entries():
            feed.append(item)

        ET.indent(feed)
        xml = ET.tostring(feed, encoding='unicode', method='xml')
        return f'<?xml version="1.0" encoding="utf-8"?>\n{xml}'

    def build(self):
        with open(self.site.directory / 'www/feed.xml', 'w') as f:
            f.write(self.render())

    def to_iso_date(self, date):
        return date.replace(tzinfo=datetime.timezone.utc).isoformat()

    def title(self):
        title = ET.TreeBuilder()
        title.start('title', {})
        title.data(self.site.title)
        title.end('title')
        return title.close()

    def subtitle(self):
        subtitle = ET.TreeBuilder()
        subtitle.start('subtitle', {})
        subtitle.data(self.site.subtitle)
        subtitle.end('subtitle')
        return subtitle.close()

    def author(self):
        author = ET.TreeBuilder()
        author.start('author', {})
        author.start('name', {})
        author.data(self.site.author)
        author.end('name')
        author.start('email', {})
        author.data(self.site.email)
        author.end('email')
        author.end('author')
        return author.close()

    def links(self) -> [ET.Element]:
        elements = []
        elements.append(
            ET.Element('link',
                       href='https://www.alexrecker.com/feed.xml',
                       rel='self',
                       type='application/atom+xml'))

        elements.append(
            ET.Element('link',
                       href='https://www.alexrecker.com/',
                       rel='alternate',
                       type='text/html'))
        return elements

    def identifier(self):
        identifier = ET.TreeBuilder()
        identifier.start('id', {})
        identifier.data('https://www.alexrecker.com/feed.xml')
        identifier.end('id')
        return identifier.close()

    def updated(self):
        updated = ET.TreeBuilder()
        updated.start('updated', {})
        updated.data(self.to_iso_date(self.site.latest.date))
        updated.end('updated')
        return updated.close()

    def entries(self):
        return map(self.to_item, itertools.islice(self.site.entries, 30))

    def to_item(self, entry):
        item = ET.Element('entry')

        # entry title
        title = ET.TreeBuilder()
        title.start('title', {})
        title.data(entry.title)
        title.end('title')
        item.append(title.close())

        # entry summary
        summary = ET.TreeBuilder()
        summary.start('summary', {})
        summary.data(entry.description)
        summary.end('summary')
        item.append(summary.close())

        # entry updated/published
        for element in ['published', 'updated']:
            tree = ET.TreeBuilder()
            tree.start(element, {})
            tree.data(self.to_iso_date(entry.date))
            tree.end(element)
            item.append(tree.close())

        # entry author
        item.append(self.author())

        # entry ID/link
        permalink = f'https://www.alexrecker.com/{entry.filename}'
        item.append(ET.Element('link', href=permalink))
        identifier = ET.TreeBuilder()
        identifier.start('id', {})
        identifier.data(permalink)
        identifier.end('id')
        item.append(identifier.close())

        if entry.banner:
            banner_url = f'https://www.alexrecker.com/images/banners/{entry.banner}'
            item.append(
                ET.Element('media:thumbnail',
                           attrib={
                               'xmlns:media': 'http://search.yahoo.com/mrss/',
                               'url': banner_url,
                           }))
            item.append(
                ET.Element('media:content',
                           attrib={
                               'medium': 'image',
                               'xmlns:media': 'http://search.yahoo.com/mrss/',
                               'url': banner_url,
                           }))

        return item
