import collections
import contextlib
import datetime
import datetime
import html
import logging
import logging
import pathlib
import pathlib
import re
import urllib.parse
import xml.etree.ElementTree

from .renderer import Renderer

logger = logging.getLogger(__name__)


def is_not_junk_file(path: str | pathlib.Path):
    """Returns true if the file is not a hidden file or an auto-save file.

    >>> is_not_junk_file(pathlib.Path('test.html'))
    True

    >>> is_not_junk_file(pathlib.Path('#.test.html'))
    False

    >>> is_not_junk_file(pathlib.Path('.test.html'))
    False
    """
    path = pathlib.Path(path)
    first_char = path.name[0]
    return first_char not in ('#', '.')


Pagination = collections.namedtuple('Pagination', ['next', 'previous'])


def paginate_files(files: list = []) -> list[Pagination]:
    """Returns a pagination map for a list of files.

    >>> pages = paginate_files(['a', 'b', 'c'])
    >>> pages['a'].previous is None
    True
    >>> pages['a'].next
    'b'
    >>> pages['c'].previous
    'b'
    >>> pages['c'].next is None
    True
    """

    pagination = {}

    for i, this_file in enumerate(files):
        kwargs = {}

        if i > 0:
            kwargs['previous'] = pathlib.Path(files[i - 1]).name
        else:
            kwargs['previous'] = None

        try:
            kwargs['next'] = pathlib.Path(files[i + 1]).name
        except IndexError:
            kwargs['next'] = None

        pagination[pathlib.Path(this_file).name] = Pagination(**kwargs)

    return pagination


Entry = collections.namedtuple('Entry', [
    'filename', 'title', 'date', 'source', 'banner', 'description',
    'page_next', 'page_previous'
])
"""Entry object."""


def new_entry(path, pagination={}) -> Entry:
    """Create an Entry (namedtuple) from a path."""

    path = pathlib.Path(path)

    # parse metadata
    metadata = re.compile(
        r'^\s?<!--\s?meta:(?P<key>[A-za-z]+)\s?(?P<value>.*)\s?-->$',
        re.MULTILINE)
    with path.open() as f:
        metadata = [(k, v) for k, v in metadata.findall(f.read())]
    metadata = dict([(k.strip(), v.strip()) for k, v in metadata])

    date = datetime.datetime.strptime(path.stem, '%Y-%m-%d')
    title = date.strftime('%A, %B %-d %Y')

    entry = Entry(filename=path.name,
                  title=title,
                  date=date,
                  source=path,
                  banner=metadata.get('banner'),
                  description=metadata['title'],
                  page_next=pagination[path.name].next,
                  page_previous=pagination[path.name].previous)

    return entry


def all_entries(entries_dir) -> list[Entry]:
    """Return all journal entries.

    Default order is latest entry first.
    """

    entries = pathlib.Path(entries_dir).glob('*.html')
    entries = filter(is_not_junk_file, entries)
    entries = sorted(entries, reverse=True)

    pages = paginate_files(entries)
    entries = [new_entry(e, pagination=pages) for e in entries]

    return entries


def render_entry(page,
                 content='',
                 full_url='',
                 author='',
                 year=datetime.datetime.now().year):
    r = Renderer()

    with r.wrapping_block('head'):
        r.block('title', contents=page.title)
        r.newline()

        r.comment('Page Assets')
        r.link(rel='shortcut icon', _type='image/x-icon', href='./favicon.ico')
        r.link(rel='stylesheet', href='./assets/site.css')
        r.newline()

        r.comment('Page Metadata')
        r.meta(charset='UTF-8')
        r.meta(name='viewport', content='width=device-width, initial-scale=1')
        r.meta(name='twitter:title', content=page.title)
        r.meta(name='twitter:description', content=page.description)
        r.meta(name='og:url',
               content=urllib.parse.urljoin(full_url, page.filename))
        r.meta(_property='og:type', content='article')
        r.meta(_property='og:title', content=page.title)
        r.meta(_property='og:description', content=page.description)
        if page.banner:
            r.meta_banner(page.banner, full_url)
        r.newline()

    r.newline()
    with r.wrapping_block('body'):
        with r.wrapping_block('article'):
            r.newline()

            r.comment('Page Header')
            r.header(title=page.title, description=page.description)

            r.divider()

            r.comment('Page Breadcrumbs')
            r.breadcrumbs(filename=page.filename)

            r.divider()

            if page.banner:
                r.comment('Page Banner')
                r.banner(page.banner)
                r.newline()

            r.comment('Begin Page Content')
            r.article(content=content)
            r.comment('End Page Content')
            r.newline()

            if page.page_next or page.page_previous:
                r.comment('Pagination')
                r.pagination(next_page=page.page_next,
                             prev_page=page.page_previous)

        r.divider()

        r.comment('Page Footer')
        r.footer(author=author, year=year)
        r.newline()

    return r.as_html()


def write_entries(entries, dir_www: str, full_url: str, author: str,
                  year: int):
    for i, entry in enumerate(entries):
        with open(entry.source, 'r') as f:
            content = f.read()

        content = render_entry(page=entry,
                               content=content,
                               full_url=full_url,
                               author=author,
                               year=year)

        target = pathlib.Path(dir_www) / entry.filename
        with open(target, 'w') as f:
            f.write(content)
            logger.debug('rendered %s', target)

        if i != 0 and i % 100 == 0:
            logger.info('rendered %d out of %d entries', i + 1, len(entries))
