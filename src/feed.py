"""generate journal RSS feed """

import logging
import urllib.parse

from . import utils

logger = logging.getLogger(__name__)


def main(args, entries=[]):
    entries = entries or utils.fetch_entries(args.directory / 'entries')

    xml = utils.StringWriter()
    xml.write('<?xml version="1.0" encoding="utf-8"?>')
    with xml.block('feed', xmlns='http://www.w3.org/2005/Atom'):
        xml.write(f'<title>{args.title}</title>')
        xml.write(f'<subtitle>{args.subtitle}</subtitle>')
        with xml.block('author'):
            xml.write(f'<name>{args.author}</name>')
            xml.write(f'<email>{args.email}</email>')

        timestamp = entries[0].date
        xml.write(f'<updated>{utils.to_iso_date(timestamp)}</updated>')

        url = args.full_url.geturl()
        feed_url = urllib.parse.urljoin(url, 'feed.xml')
        xml.write(
            f'<link href="{feed_url}" rel="self" type="application/atom+xml" />'
        )
        xml.write(f'<link href="{url}" rel="alternate" type="text/html" />')
        xml.write(f'<id>{feed_url}</id>')

        for entry in entries:
            with xml.block('entry'):
                xml.write(f'<title>{entry.title}</title>')

                xml.write(
                    f'<summary><![CDATA[{entry.description}]]></summary>')

                timestamp = utils.to_iso_date(entry.date)
                xml.write(f'<published>{timestamp}</published>')
                xml.write(f'<updated>{timestamp}</updated>')

                with xml.block('author'):
                    xml.write(f'<name>{args.author}</name>')
                    xml.write(f'<email>{args.email}</email>')

                entry_url = urllib.parse.urljoin(url, entry.filename)
                xml.write(f'<link href="{entry_url}" />')
                xml.write(f'<id>{entry_url}</id>')
                if entry.banner:
                    banner_url = urllib.parse.urljoin(
                        url, f'images/banners/{entry.banner}')
                    xml.write(
                        f'<media:thumbnail xmlns:media="http://search.yahoo.com/mrss/" url="{banner_url}" />'
                    )
                    xml.write(
                        f'<media:content medium="image" xmlns:media="http://search.yahoo.com/mrss/" url="{banner_url}" />'
                    )

    with utils.write_page(args.directory,
                          'feed.xml',
                          overwrite_ok=args.overwrite) as f:
        f.write(xml.text)
    logger.info('generated %s with %d entries', 'feed.xml', len(entries))
