import collections
import copy
import datetime
import functools
import logging
import pathlib
import random
import re

from .renderer import Renderer

logger = logging.getLogger(__name__)

Page = collections.namedtuple('Page', [
    'filename',
    'title',
    'description',
    'banner',
    'render_func',
])
PAGES = {}


def register_page(filename='', title='', description='', banner=''):
    def wrapper(func):
        functools.wraps(func)
        PAGES[filename] = Page(filename=filename,
                               title=title,
                               description=description,
                               banner=banner,
                               render_func=func)
        return func

    return wrapper


Entry = collections.namedtuple('Entry', [
    'filename', 'title', 'description', 'banner', 'date', 'source',
    'page_next', 'page_previous'
])


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


Pagination = collections.namedtuple('Pagination', ['next', 'previous'])


def paginate_files(files=[]):
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


def is_not_junk_file(path):
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


def fetch_entries(entries_dir: str):
    entries = pathlib.Path(entries_dir).glob('*.html')
    entries = filter(is_not_junk_file, entries)
    entries = sorted(entries, reverse=True)
    pages = paginate_files(entries)
    entries = [new_entry(e, pagination=pages) for e in entries]
    logger.info('fetched %d entries from %s', len(entries), entries_dir)
    return entries


def fetch_pages():
    pages = [PAGES[k] for k in sorted(PAGES.keys())]
    logger.info('fetched %d pages', len(pages))
    return pages


def render_page(page,
                full_url='',
                author='',
                year=datetime.datetime.now().year,
                entries=[],
                pages=[],
                args=None,
                c=None):

    r = Renderer()

    r.head(filename=page.filename,
           title=page.title,
           description=page.description,
           banner=page.banner,
           full_url=full_url)

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
            r.article(content=page.render_func(
                renderer=Renderer(), args=args, entries=entries, pages=pages, c=c))
            r.comment('End Page Content')
            r.newline()

        r.divider()

        r.comment('Page Footer')
        r.footer(author=author, year=year)
        r.newline()

    return r.as_html()


def render_entry(page,
                 content='',
                 full_url='',
                 author='',
                 year=datetime.datetime.now().year):
    r = Renderer()

    r.head(filename=page.filename,
           title=page.title,
           description=page.description,
           banner=page.banner,
           full_url=full_url)

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


def write_pages(dir_www,
                full_url,
                author='',
                year=datetime.datetime.now().year,
                entries=[],
                pages=[],
                args=None,
                c=None):
    for i, page in enumerate(pages):
        logger.info('writing %s [page %d/%d]', page.filename, i + 1,
                    len(pages))
        target = pathlib.Path(dir_www) / page.filename
        with open(target, 'w') as f:
            content = render_page(page,
                                  full_url=full_url,
                                  year=year,
                                  author=author,
                                  entries=entries,
                                  pages=pages,
                                  args=args,
                                  c=c)
            f.write(content)


def write_entries(entries,
                  dir_www: str,
                  full_url: str,
                  author: str,
                  year=None):
    for entry in entries:
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

    logger.info('wrote %d entries', len(entries))
