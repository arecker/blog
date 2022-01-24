"""Functions for building and maniupulating XML elements."""

from xml.etree import ElementTree as ET
from urllib.parse import urljoin
import datetime


def new_feed(title='',
             subtitle='',
             author='',
             email='',
             timestamp='',
             feed_uri='',
             site_uri=''):
    root = ET.Element('feed', xmlns='http://www.w3.org/2005/Atom')

    element = ET.TreeBuilder()
    element.start('title', {})
    element.data(title)
    element.end('title')
    root.append(element.close())

    element = ET.TreeBuilder()
    element.start('subtitle', {})
    element.data(subtitle)
    element.end('subtitle')
    root.append(element.close())

    root.append(build_author(name=author, email=email))

    element = ET.TreeBuilder()
    element.start('updated', {})
    element.data(to_iso_date(timestamp))
    element.end('updated')
    root.append(element.close())

    element = ET.Element('link',
                         href=feed_uri,
                         rel='self',
                         type='application/atom+xml')
    root.append(element)

    element = ET.Element('link',
                         href=site_uri,
                         rel='alternate',
                         type='text/html')
    root.append(element)

    element = ET.TreeBuilder()
    element.start('id', {})
    element.data(feed_uri)
    element.end('id')
    root.append(element.close())

    return root


def build_author(name='', email=''):
    element = ET.TreeBuilder()
    element.start('author', {})
    element.start('name', {})
    element.data(name)
    element.end('name')
    element.start('email', {})
    element.data(email)
    element.end('email')
    element.end('author')
    return element.close()


def new_sitemap():
    attributes = {
        'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        'xsi:schemaLocation':
        'http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd',
        'xmlns': 'http://www.sitemaps.org/schemas/sitemap/0.9'
    }
    return ET.Element('urlset', attrib=attributes)


def stringify_xml(xml_tree, prettify=True):
    if prettify:
        ET.indent(xml_tree)
    xml = ET.tostring(xml_tree, encoding='unicode', method='xml')
    return f'<?xml version="1.0" encoding="utf-8"?>\n{xml}'


def as_location_elements(locations=[]):
    for location, date in locations:
        url = ET.TreeBuilder()
        url.start('url', {})
        url.start('loc', {})
        url.data(location)
        url.end('loc')
        url.start('lastmod', {})
        url.data(to_iso_date(date))
        url.end('lastmod')
        url.end('url')
        yield url.close()


def as_feed_entry(entry, author='', email='', full_url=''):
    item = ET.Element('entry')
    assert all([author, email, full_url]), 'required!'

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
        tree.data(to_iso_date(entry.date))
        tree.end(element)
        item.append(tree.close())

    # entry author
    author = build_author(name=author, email=email)
    item.append(author)

    # entry ID/link
    permalink = f'{full_url.scheme}://{full_url.netloc}/{entry.filename}'
    item.append(ET.Element('link', href=permalink))
    identifier = ET.TreeBuilder()
    identifier.start('id', {})
    identifier.data(permalink)
    identifier.end('id')
    item.append(identifier.close())

    if entry.banner:
        banner_url = urljoin(
            f'{full_url.scheme}://{full_url.netloc}{full_url.path}',
            f'images/banners/{entry.banner}')
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


def to_iso_date(date):
    return date.replace(tzinfo=datetime.timezone.utc).isoformat()
