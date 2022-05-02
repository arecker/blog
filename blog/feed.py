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
