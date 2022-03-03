"""generate journal RSS feed """

import collections
import html
import logging
import pathlib
import urllib.parse

from . import utils

logger = logging.getLogger(__name__)

FeedInfo = collections.namedtuple(
    'FeedInfo', ['url', 'email', 'author', 'title', 'subtitle', 'timestamp'])


def render_info(sw: utils.StringWriter, info: FeedInfo) -> utils.StringWriter:
    """Render RSS feed info portion."""
    sw.write(f'<title>{info.title}</title>')
    sw.write(f'<subtitle>{info.subtitle}</subtitle>')

    with sw.block('author'):
        sw.element('name', info.author)
        sw.element('email', info.email)

    sw.element('updated', utils.to_iso_date(info.timestamp))

    assert isinstance(info.url, urllib.parse.ParseResult)
    url = info.url.geturl()
    feed_url = urllib.parse.urljoin(url, 'feed.xml')
    sw.element('id', feed_url)
    sw.link(href=feed_url, rel='self', _type='application/atom+xml')
    sw.link(href=url, rel='alternate', _type='text/html')

    return sw


def render_entry(sw: utils.StringWriter, entry: utils.Entry, info: FeedInfo,
                 directory: pathlib.Path) -> utils.StringWriter:

    with sw.block('entry'):
        sw.element('title', entry.title)
        sw.element('summary', f'<![CDATA[{entry.description}]]>')

        timestamp = utils.to_iso_date(entry.date)
        sw.element('published', timestamp)
        sw.element('updated', timestamp)

        with sw.block('author'):
            sw.element('name', info.author)
            sw.element('email', info.email)

        url = info.url.geturl()
        entry_url = urllib.parse.urljoin(url, entry.filename)
        sw.element('id', entry_url)
        sw.write(f'<link href="{entry_url}" />')

        if entry.banner:
            banner_url = urllib.parse.urljoin(
                url, f'images/banners/{entry.banner}')
            url = f'url="{banner_url}"'
            schema = 'xmlns:media="http://search.yahoo.com/mrss/"'
            sw.write(f'<media:thumbnail {schema} {url} />')
            sw.write(f'<media:content medium="image" {schema} {url} />')

        with open(directory / f'entries/{entry.filename}', 'r') as f:
            content = f.read()
            content = html.escape(content)
            content = f'<![CDATA[{content}]]>'
            sw.element('content', content)

    return sw


def main(args, entries=[]):
    entries = entries or utils.fetch_entries(args.directory / 'entries')

    xml = utils.StringWriter()
    xml.write('<?xml version="1.0" encoding="utf-8"?>')

    with xml.block('feed', xmlns='http://www.w3.org/2005/Atom'):

        # Render info
        info = FeedInfo(url=args.full_url,
                        email=args.email,
                        author=args.author,
                        title=args.title,
                        subtitle=args.subtitle,
                        timestamp=entries[0].date)
        xml = render_info(xml, info)

        # Render entries
        for entry in entries[0:30]:
            xml = render_entry(xml, entry, info, args.directory)

    with utils.write_page(args.directory, 'feed.xml', overwrite_ok=True) as f:
        f.write(xml.text)
    logger.info('generated %s with %d entries', 'feed.xml', len(entries))
