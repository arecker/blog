from xml.etree import ElementTree as ET
import datetime


def build_feed_entry(page, config):
    entry = ET.Element('entry')

    # entry title
    title = ET.TreeBuilder()
    title.start('title', {})
    title.data(page.title)
    title.end('title')
    entry.append(title.close())

    # entry summary
    summary = ET.TreeBuilder()
    summary.start('summary', {})
    summary.data(page.description)
    summary.end('summary')
    entry.append(summary.close())

    # entry updated/published
    for element in ['published', 'updated']:
        tree = ET.TreeBuilder()
        tree.start(element, {})
        tree.data(to_feed_date(page.date))
        tree.end(element)
        entry.append(tree.close())

    # entry author
    entry.append(build_rss_feed_author(config))

    # entry ID/link
    permalink = f'https://www.alexrecker.com/{page.filename}'
    entry.append(ET.Element('link', href=permalink))
    identifier = ET.TreeBuilder()
    identifier.start('id', {})
    identifier.data(permalink)
    identifier.end('id')
    entry.append(identifier.close())

    if page.banner:
        banner_url = f'https://www.alexrecker.com/images/banners/{page.banner}'
        entry.append(
            ET.Element('media:thumbnail',
                       attrib={
                           'xmlns:media': 'http://search.yahoo.com/mrss/',
                           'url': banner_url,
                       }))
        entry.append(
            ET.Element('media:content',
                       attrib={
                           'medium': 'image',
                           'xmlns:media': 'http://search.yahoo.com/mrss/',
                           'url': banner_url,
                       }))

    return entry


def build_rss_feed(entries=[], config=None, context=None) -> str:
    feed = ET.Element('feed', xmlns='http://www.w3.org/2005/Atom')

    # title
    title = ET.TreeBuilder()
    title.start('title', {})
    title.data(config['site']['title'])
    title.end('title')
    feed.append(title.close())

    # subtitle
    subtitle = ET.TreeBuilder()
    subtitle.start('subtitle', {})
    subtitle.data(config['site']['subtitle'])
    subtitle.end('subtitle')
    feed.append(subtitle.close())

    # author
    feed.append(build_rss_feed_author(config))

    # links
    feed.append(
        ET.Element('link',
                   href='https://www.alexrecker.com/feed.xml',
                   rel='self',
                   type='application/atom+xml'))
    feed.append(
        ET.Element('link',
                   href='https://www.alexrecker.com/',
                   rel='alternate',
                   type='text/html'))

    # id
    identifier = ET.TreeBuilder()
    identifier.start('id', {})
    identifier.data('https://www.alexrecker.com/feed.xml')
    identifier.end('id')
    feed.append(identifier.close())

    # updated
    updated = ET.TreeBuilder()
    updated.start('updated', {})
    updated.data(to_feed_date(context.latest.date))
    updated.end('updated')
    feed.append(updated.close())

    # entries
    for page in reversed(context.entries[-30:]):
        entry = build_feed_entry(page, config)
        feed.append(entry)

    ET.indent(feed)
    xml = ET.tostring(feed, encoding='unicode', method='xml')
    return f'<?xml version="1.0" encoding="utf-8"?>\n{xml}'


def build_sitemap(context=None):
    sitemap = ET.Element(
        'urlset',
        attrib={
            'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
            'xsi:schemaLocation':
            'http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd',
            'xmlns': 'http://www.sitemaps.org/schemas/sitemap/0.9'
        })

    for page in context.entries + context.pages:
        url = ET.TreeBuilder()
        url.start('url', {})
        url.start('loc', {})
        url.data(f'https://www.alexrecker.com/{page.filename}')
        url.end('loc')

        if page.is_entry():
            url.start('lastmod', {})
            url.data(to_feed_date(page.date))
            url.end('lastmod')

        url.end('url')

        sitemap.append(url.close())

    ET.indent(sitemap)
    xml = ET.tostring(sitemap, encoding='unicode', method='xml')
    return f'<?xml version="1.0" encoding="utf-8"?>\n{xml}'


def build_rss_feed_author(config):
    author = ET.TreeBuilder()
    author.start('author', {})
    author.start('name', {})
    author.data(config['site']['author'])
    author.end('name')
    author.start('email', {})
    author.data(config['site']['email'])
    author.end('email')
    author.end('author')
    return author.close()


def to_feed_date(timestamp):
    return timestamp.replace(tzinfo=datetime.timezone.utc).isoformat()
