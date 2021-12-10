"""Functions for building and maniupulating XML elements."""

from xml.etree import ElementTree as ET
import datetime


def new_feed():
    return ET.Element('feed', xmlns='http://www.w3.org/2005/Atom')


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


def to_iso_date(date):
    return date.replace(tzinfo=datetime.timezone.utc).isoformat()
