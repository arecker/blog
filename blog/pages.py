import collections
import datetime
import functools
import json
import logging
import pathlib
import random

from .renderer import Renderer

logger = logging.getLogger(__name__)

PAGES = {}

Page = collections.namedtuple('Page', [
    'filename',
    'title',
    'description',
    'banner',
    'render_func',
])


def register_page(filename='', title='', description='', banner=''):
    def wrapper(func):
        functools.wraps(func)
        logger.debug('registering %s page to %s', filename, func)
        PAGES[filename] = Page(filename=filename,
                               title=title,
                               description=description,
                               banner=banner,
                               render_func=func)
        return func

    return wrapper


def register_page_from_data(path: str):
    path = pathlib.Path(path)
    with open(path, 'r') as f:
        data = json.load(f)
    logger.debug('imported data from %s', path)

    def render_func(*args, **kwargs):
        return f'Rendered version of {path.name}'

    page = Page(
        filename=data['filename'],
        title=data['title'],
        description=data['description'],
        banner=data.get('banner'),
        render_func=render_func,
    )

    PAGES[page.filename] = page


def render_page(page,
                full_url='',
                author='',
                year=datetime.datetime.now().year,
                entries=[],
                pages=[]):

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
            r.article(content=page.render_func(entries=entries, pages=pages))
            r.comment('End Page Content')
            r.newline()

        r.divider()

        r.comment('Page Footer')
        r.footer(author=author, year=year)
        r.newline()

    return r.as_html()


@register_page(filename='index.html',
               title='Dear Journal',
               description='Daily, public journal by Alex Recker')
def index(entries=[], pages=[]):
    r = Renderer()

    latest = entries[0]
    r.block('h2', 'Latest Entry 📣')
    r.block('strong', latest.title)
    r.figure(alt='latest entry banner',
             src=f'./images/banners/{latest.banner}',
             href=f'./{latest.filename}',
             caption=latest.description)

    r.divider()

    choices = [e for e in entries if e.banner]
    choice = random.choice(choices)
    r.block('h2', 'Random Entry 🎲')
    r.block('strong', choice.title)
    r.figure(alt='latest entry banner',
             src=f'./images/banners/{choice.banner}',
             href=f'./{choice.filename}',
             caption=choice.description)

    r.divider()

    r.block('h2', 'Feeds 🛰')
    with r.wrapping_block('table'):
        with r.wrapping_block('tr'):
            with r.wrapping_block('td'):
                r.block('a', href='./feed.xml', contents='feed.xml')
            r.block('td', contents='journal entries Atom feed (latest 50)')

    r.divider()

    r.block('h2', 'Pages 🗺')
    pages = [p for p in pages if p.filename != 'index.html']
    with r.wrapping_block('table'):
        for page in pages:
            with r.wrapping_block('tr'):
                with r.wrapping_block('td'):
                    r.block('a',
                            href=f'./{page.filename}',
                            contents=page.filename)
                r.block('td', contents=page.description)

    return r.text


@register_page(filename='entries.html',
               title='Entries',
               description='complete archive of journal entries')
def entries_page(entries=[], pages=[]):
    r = Renderer()

    entries_with_banners = [e for e in entries if e.banner]
    choice = random.choice(entries_with_banners)
    r.figure(alt='random banner',
             src=f'./images/banners/{choice.banner}',
             href=f'./{choice.filename}',
             caption=f'taken from {choice.title}, "{choice.description}"')

    with r.wrapping_block('table'):
        for entry in entries:
            with r.wrapping_block('tr'):
                with r.wrapping_block('td'):
                    r.block('a',
                            href=f'./{entry.filename}',
                            contents=f'{entry.filename}')
                r.block('td', contents=entry.description)

    return r.text


def write_pages(dir_www='',
                dir_data='',
                full_url='',
                author='',
                year=None,
                entries=[]):
    for data in pathlib.Path(dir_data).glob('*.json'):
        register_page_from_data(data)

    pages = sorted(PAGES.values(), key=lambda p: p.filename)
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
                                  pages=pages)
            f.write(content)
