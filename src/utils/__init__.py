"""Package for random functions."""
from .string_writer import StringWriter

import blog
import collections
import datetime
import json
import logging
import pathlib
import platform
import typing
import urllib.parse

logger = logging.getLogger(__name__)


def read_nav(data_dir: pathlib.Path):
    with open(data_dir / 'nav.json', 'r') as f:
        return json.load(f)


def to_iso_date(date):
    return date.replace(tzinfo=datetime.timezone.utc).isoformat()


Page = collections.namedtuple(
    'Page',
    [
        'filename',
        'title',
        'description',
        'banner',
    ],
)


def render_page(
        page: typing.Union[Page, blog.Entry],
        full_url: urllib.parse.ParseResult,
        content='',
        nav_pages=[],
        copyright_year=datetime.datetime.now().year,
        python_version=platform.python_version(),
        author=None,
) -> str:
    """Render an HTML page as a string."""

    html = StringWriter()

    html.write('<!doctype html>')
    html.write('<html lang="en">', blank=True)

    page_url = urllib.parse.urljoin(full_url.geturl(), page.filename)
    with html.block('head', blank=True):
        html.write(f'<title>{page.title}</title>', blank=True)

        html.comment('Page Assets')
        html.write(
            '<link rel="shortcut icon" type="image/x-icon" href="./favicon.ico"/>'
        )
        html.write('<link href="./assets/site.css" rel="stylesheet"/>',
                   blank=True)

        html.comment('Page Metadata')
        html.write('<meta charset="UTF-8"/>')
        html.meta(name='viewport',
                  content='width=device-width, initial-scale=1')
        html.meta(name='twitter:title', content=page.title)
        html.meta(name='twitter:description', content=page.description)
        html.meta(_property='og:url', content=page_url)
        html.meta(_property='og:type', content='article')
        html.meta(_property='og:title', content=page.title)
        html.meta(_property='og:description', content=page.description)
        if page.banner:
            banner = urllib.parse.urljoin(full_url.geturl(),
                                          f'/images/banners/{page.banner}')
            html.meta(name='image', _property='og:image', content=banner)
            html.meta(name='twitter:image', content=banner)
        with html.indentation_reset():
            html.write('')

    with html.block('body', _id='top', blank=True):
        html.blank()
        html.comment('Site Navigation')
        with html.block('nav', blank=True):
            for nav_page in nav_pages:
                html.write(f'<a href="./{nav_page}">{nav_page}</a>')
            html.br()
            html.write('<a href="./index.html">index.html</a>')
            if page.filename != 'index.html':
                html.write(f'<span>/ {page.filename}</span>')

        with html.block('article', blank=True):
            html.blank()

            html.comment('Page Header')
            with html.block('header', blank=True):
                html.write(f'<h1>{page.title}</h1>')
                html.p(page.description, blank=False)

            html.hr()

            if page.banner:
                html.comment('Page Banner')
                html.figure(src=f'./images/banners/{page.banner}',
                            alt='banner',
                            blank=True)

            with html.indentation_reset():
                html.write(content, blank=True)

        html.hr()

        html.comment('Site Footer')
        with html.block('footer', blank=True):
            # Back to top
            html.write('<small><a href="#top">Back to top</a></small>')
            html.br()

            # Validate HTML
            validate_url = urllib.parse.urljoin(full_url.geturl(),
                                                page.filename)
            validate_url = urllib.parse.quote(validate_url)
            validate_url = f'https://validator.w3.org/nu/?doc={validate_url}'
            html.small(f'<a href="{validate_url}">Validate this page</a>')
            html.br()

            # Software Info
            link = f'<a href="./blog.html">blog</a>'
            html.small(f'Built with {link} and Python v{python_version}')
            html.br()

            # Copyright Info
            html.small(f'© Copyright {copyright_year} {author}')

    html.write('</html>')

    return html.text
