import collections
import datetime
import urllib.parse

from .renderer import Renderer

Info = collections.namedtuple('Info', [
    'title',
    'subtitle',
    'author_name',
    'author_email',
    'timestamp',
    'full_url',
])


def render_feed_info(info: Info) -> str:
    assert isinstance(info.full_url, str), 'full_url should be a string'

    r = Renderer()

    r.block('title', info.title)
    r.block('subtitle', info.subtitle)
    with r.wrapping_block('author'):
        r.block('name', info.author_name)
        r.block('email', info.author_email)

    timestamp = info.timestamp.replace(
        tzinfo=datetime.timezone.utc).isoformat()
    r.block('updated', timestamp)
    r.block('id', contents=urllib.parse.urljoin(info.full_url, 'feed.xml'))
    r.link(
        rel='self',
        _type='application/atom+xml',
        href=urllib.parse.urljoin(info.full_url, 'feed.xml'),
    )
    r.link(
        rel='alternate',
        _type='text/html',
        href=info.full_url,
    )
    return r.text


def render_feed_entry(entry, info: Info):
    r = Renderer()

    with r.wrapping_block('entry'):
        r.block('title', entry.title)
        r.block('summary', contents=entry.description, cdata=True)

        timestamp = entry.date.replace(
            tzinfo=datetime.timezone.utc).isoformat()
        r.block('published', contents=timestamp)
        r.block('updated', contents=timestamp)

        with r.wrapping_block('author'):
            r.block('name', info.author_name)
            r.block('email', info.author_email)

        url = urllib.parse.urljoin(info.full_url, entry.filename)
        r.block('id', url)
        r.link(href=url)

        if entry.banner:
            banner_url = f'images/banners/{entry.banner}'
            banner_url = urllib.parse.urljoin(info.full_url, banner_url)
            attrs = {
                'self_closing': True,
                'url': banner_url,
                'xmlns:media': 'http://search.yahoo.com/mrss/',
            }
            r.block('media:thumbnail', **attrs)
            r.block('media:content', medium='image', **attrs)

        with open(entry.source, 'r') as f:
            r.block('content', cdata=True, contents=f.read())

    return r.text
