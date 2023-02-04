import collections
import datetime
import html
import logging
import pathlib
import re
import urllib.parse

from .renderer import Renderer

logger = logging.getLogger(__name__)

Info = collections.namedtuple('Info', [
    'title',
    'subtitle',
    'author_name',
    'author_email',
    'timestamp',
    'full_url',
])

Item = collections.namedtuple('Item', [
    'banner',
    'date',
    'description',
    'filename',
    'source',
    'title',
])


def plain_textify(content: str) -> str:

    # strip out paragraphs
    pattern = re.compile(r'^\<p\>(.*)\<\/p\>$', re.MULTILINE)
    content = pattern.sub(r'\1', content)

    # strip out b's, em's, and strong's
    tags = ['b', 'em', 'strong']
    tags = [f'<{t}>' for t in tags] + [f'</{t}>' for t in tags]
    for tag in tags:
        content = content.replace(tag, '')

    # strip out links
    pattern = re.compile(r'<a href=\".*?\">(.*?)</a>')
    content = pattern.sub(r'[\1]', content)

    # strip out comments
    pattern = re.compile(r'^<!--.*-->$', re.MULTILINE)
    content = pattern.sub('', content)

    # strip out figures
    pattern = re.compile(
        r'<figure>\n  <a href=\".*?\">\n    <img .*?alt=\"(.*?)\" .*?/>\n  \</a>\n</figure>',
        re.DOTALL)
    content = pattern.sub(r'[figure \1]', content)

    # figures with captions
    pattern = re.compile(
        r'<figure>\n  <a href=\".*?\">\n    <img .*?alt=\"(.*?)\" .*?/>\n  \</a>\n  <figcaption><p>(.*?)</p></figcaption>\n</figure>',
        re.DOTALL)
    content = pattern.sub(r'[figure \1: \2]', content)

    # strip out video
    pattern = re.compile(
        r'<video .*?>\n  <source src=\"\.?\/vids\/\d{4}-\d{2}-\d{2}-(.*?)\..*?/>.*?</video>',
        re.DOTALL,
    )
    content = pattern.sub(r'[video \1]', content)

    return content


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


def render_feed_entry(item, info: Info):
    r = Renderer(starting_indent_level=2)

    with r.wrapping_block('entry'):
        if item.title:
            r.block('title', item.title)
        if item.description:
            r.block('summary', contents=item.description, cdata=True)

        timestamp = item.date.replace(
            tzinfo=datetime.timezone.utc).isoformat()
        r.block('published', contents=timestamp)
        r.block('updated', contents=timestamp)

        with r.wrapping_block('author'):
            r.block('name', info.author_name)
            r.block('email', info.author_email)

        url = urllib.parse.urljoin(info.full_url, item.filename)
        r.block('id', url)
        r.link(href=url)

        if item.banner:
            banner_url = f'images/banners/{item.banner}'
            banner_url = urllib.parse.urljoin(info.full_url, banner_url)
            attrs = {
                'self_closing': True,
                'url': banner_url,
                'xmlns:media': 'http://search.yahoo.com/mrss/',
            }
            r.block('media:thumbnail', **attrs)
            r.block('media:content', medium='image', **attrs)

        if item.source:
            with open(item.source, 'r') as f:
                contents = f.read()
                contents = plain_textify(contents)
                contents = '\n' + contents.strip() + '\n'
                contents = html.escape(contents)
                r.block('content', cdata=True, contents=contents)

    return r.text


def render_feed(info: Info, items=[]) -> str:
    r = Renderer()

    with r.wrapping_block('feed', xmlns='http://www.w3.org/2005/Atom'):
        for line in render_feed_info(info).splitlines():
            r.write(line)

        for item in items:
            for line in render_feed_entry(item, info).splitlines():
                r.text += line + '\n'

    return r.as_xml()


def write_feed(www_dir,
               title='',
               subtitle='',
               author_name='',
               author_email='',
               timestamp='',
               full_url='',
               entries=[]):

    info = Info(title=title,
                subtitle=subtitle,
                author_name=author_name,
                author_email=author_email,
                timestamp=timestamp,
                full_url=full_url)

    items = []
    for entry in entries:
        items.append(Item(
            banner=f'banners/{entry.banner}',
            date=entry.date,
            description=entry.description,
            filename=entry.filename,
            source=entry.source,
            title=entry.title,
        ))

    www_dir = pathlib.Path(www_dir)
    for p in www_dir.glob('images/*.*'):
        slug = p.name[:10] # YYYY-MM-dd-blah.jpg
        title = slug + ' - ' + p.stem[11:].replace('-', ' ').title()
        date = datetime.datetime.strptime(slug, '%Y-%m-%d')
        banner = str(p.relative_to(www_dir))
        items.append(Item(
            banner=banner,
            date=date,
            description='',
            filename=banner,
            source='',
            title=title,
        ))

    items = list(sorted(items, key=lambda i: i.date, reverse=True))
    items = items[:500]

    target = www_dir / 'feed.xml'

    with target.open('w') as f:
        f.write(render_feed(info, items))
    logger.info('wrote feed to %s with %d item(s)', target, len(items))
