"""generate journal RSS feed """

import logging
import urllib.parse

from . import utils

logger = logging.getLogger(__name__)


def render_info(title='',
                subtitle='',
                author='',
                email='',
                full_url=None,
                timestamp=None) -> str:
    url = full_url.geturl()
    feed_url = urllib.parse.urljoin(url, 'feed.xml')

    return f"""  <title>{title}</title>
  <subtitle>{subtitle}</subtitle>
  <author>
    <name>{author}</name>
    <email>{email}</email>
  </author>
  <updated>{utils.to_iso_date(timestamp)}</updated>
  <link href="{feed_url}" rel="self" type="application/atom+xml" />
  <link href="{url}" rel="alternate" type="text/html" />
  <id>{feed_url}</id>"""


def render_entry(entry: utils.Entry, author='', email='', full_url=None):
    timestamp = utils.to_iso_date(entry.date)
    url = urllib.parse.urljoin(full_url.geturl(), entry.filename)

    if entry.banner:
        banner_url = urllib.parse.urljoin(full_url.geturl(),
                                          f'images/banners/{entry.banner}')
        banner_data = f"""    <media:thumbnail xmlns:media="http://search.yahoo.com/mrss/" url="{banner_url}" />
    <media:content medium="image" xmlns:media="http://search.yahoo.com/mrss/" url="{banner_url}" />"""
    else:
        banner_data = ""

    return f"""  <entry>
    <title>{entry.title}</title>
    <summary>{entry.description}</summary>
    <published>{timestamp}</published>
    <updated>{timestamp}</updated>
    <author>
      <name>{author}</name>
      <email>{email}</email>
    </author>
    <link href="{url}" />
    <id>{url}</id>
{banner_data}
  </entry>"""


def main(args, entries=[]):
    entries = entries or utils.fetch_entries(args.directory / 'entries')
    info = render_info(
        title=args.title,
        subtitle=args.subtitle,
        author=args.author,
        email=args.email,
        full_url=args.full_url,
        timestamp=entries[0].date,
    )
    entries = '\n'.join([
        render_entry(e,
                     author=args.author,
                     email=args.email,
                     full_url=args.full_url) for e in entries
    ][:30])
    feed = f'''
<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
{info}
{entries}
</feed>
'''.lstrip()

    with open(args.directory / 'www/feed.xml', 'w') as f:
        f.write(feed)
    logger.info('generated %s', 'feed.xml')
