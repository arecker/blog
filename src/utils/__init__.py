"""Package for random functions."""
from .string_writer import StringWriter

import collections
import datetime
import json
import logging
import pathlib
import platform
import re
import typing
import urllib.parse

logger = logging.getLogger(__name__)


def read_nav(data_dir: pathlib.Path):
    with open(data_dir / 'nav.json', 'r') as f:
        return json.load(f)


Entry = collections.namedtuple('Entry', [
    'banner',
    'date',
    'description',
    'filename',
    'page_next',
    'page_previous',
    'source',
    'title',
])


def is_not_junk_file(path: pathlib.Path):
    """Returns true if the file is not a hidden file or an auto-save file.

    >>> is_not_junk_file(pathlib.Path('test.html'))
    True

    >>> is_not_junk_file(pathlib.Path('#.test.html'))
    False

    >>> is_not_junk_file(pathlib.Path('.test.html'))
    False
    """

    first_char = path.name[0]
    return first_char not in ('#', '.')


def fetch_entries(entries_dir: pathlib.Path) -> list[Entry]:
    """Returns a list of paginated entries, latest first."""

    files = sorted(entries_dir.glob('*.html'), reverse=True)
    files = list(filter(is_not_junk_file, files))
    pages = paginate_list([f.name for f in files])

    entries = []

    for source in files:
        kwargs = {}

        # Data from the file path
        kwargs['filename'] = source.name
        kwargs['source'] = source.absolute()
        kwargs['date'] = datetime.datetime.strptime(source.stem, '%Y-%m-%d')
        kwargs['title'] = kwargs['date'].strftime('%A, %B %-d %Y')

        # From the metadata
        with open(kwargs['source'], 'r') as f:
            # TODO: it sucks we have to read the file just to get the
            # metadata.  Maybe something faster?
            content = f.read()
        metadata = metadata_parse_html(content)
        kwargs['banner'] = metadata.get('banner')  # banner is optional
        kwargs['description'] = metadata['title']  # title is required

        # Set the pagination
        pagination = pages[source.name]
        kwargs['page_next'] = pagination.next
        kwargs['page_previous'] = pagination.previous

        entries.append(Entry(**kwargs))

    logger.info('parsed %d entries from %s', len(entries),
                prettify_path(entries_dir))
    return entries


def metadata_parse_html(content) -> dict:
    """Parse metadata from magic HTML comments.

    >>> metadata_parse_html('<!-- meta:name Alex Recker -->')
    {'name': 'Alex Recker'}
    """

    pattern = re.compile(
        r'^\s?<!--\s?meta:(?P<key>[A-za-z]+)\s?(?P<value>.*)\s?-->$',
        re.MULTILINE)
    values = [(k.strip(), v.strip()) for k, v in pattern.findall(content)]
    return dict(values)


Pagination = collections.namedtuple('Pagination', ['next', 'previous'])


def paginate_list(things: list = []):
    """Returns a pagination map for a list of things.

    >>> pages = paginate_list(['a', 'b', 'c'])
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

    for i, thing in enumerate(things):
        if i > 0:
            previous_thing = things[i - 1]
        else:
            previous_thing = None

        try:
            next_thing = things[i + 1]
        except IndexError:
            next_thing = None

        pagination[thing] = Pagination(next_thing, previous_thing)

    return pagination


def prettify_path(path, home=pathlib.Path.home()):
    """Render the pretty form of a path.

    Substitute '~' for the home directory.

    >>> prettify_path('/home/alex/src/blog', home=pathlib.Path('/home/alex'))
    '~/src/blog'
    """

    return re.sub(f'^{home}/', '~/', str(path))


def slugify(word):
    return word.lower().replace(" ", "-")


def month_name(month_int: int) -> str:
    """Return a month name for the integer.

    >>> month_name(6)
    'June'

    >>> month_name(1)
    'January'
    """

    date = datetime.datetime.strptime(str(month_int), '%m')
    return date.strftime('%B')


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
        page: typing.Union[Page, Entry],
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
