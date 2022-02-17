"""Some random functions."""

import collections
import contextlib
import datetime
import errno
import json
import logging
import os
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


def fetch_entries(entries_dir: pathlib.Path) -> list[Entry]:
    """Returns a list of paginated entries, latest first."""

    files = sorted(entries_dir.glob('*.html'), reverse=True)
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
    """Parse metadata from magic HTML comments."""

    pattern = re.compile(
        r'^\s?<!--\s?meta:(?P<key>[A-za-z]+)\s?(?P<value>.*)\s?-->$',
        re.MULTILINE)
    values = [(k.strip(), v.strip()) for k, v in pattern.findall(content)]
    return dict(values)


Pagination = collections.namedtuple('Pagination', ['next', 'previous'])


def paginate_list(things):
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


class StringWriter:
    def __init__(self, each_indent=2, starting_indent=0):
        self.each_indent = int(each_indent)
        self.current_indent = starting_indent
        self.text = ''

    def indent(self):
        self.current_indent += self.each_indent

    def unindent(self):
        result = self.current_indent - self.each_indent
        if result < 0:
            raise ValueError('indented too far!')
        self.current_indent = result

    def write(self,
              text,
              indent=False,
              unindent=False,
              blank=False,
              newline=True):
        padding = self.current_indent * ' '
        self.text += f'{padding}{text}'
        if newline:
            self.text += '\n'

        if blank:
            with self.indentation_reset():
                self.write('')

        if indent:
            self.indent()
        if unindent:
            self.unindent()

    @contextlib.contextmanager
    def indentation_reset(self):
        current = self.current_indent
        self.current_indent = 0
        yield
        self.current_indent = current

    def comment(self, text):
        self.write(f'<!-- {text} -->')

    @contextlib.contextmanager
    def block(self,
              element_name,
              blank=False,
              blank_before=False,
              _class='',
              _type='',
              **attributes):
        """Context manager that wraps contents in an element.

        Will reset the indentation back to its starting position, so
        do whatever you want while inside.
        """
        starting_indent = self.current_indent

        if _class:
            attributes['class'] = _class
        if _type:
            attributes['type'] = _type

        attributes = sorted([f'{k}="{v}"' for k, v in attributes.items()])
        attributes = ' '.join(attributes)
        attributes = attributes.strip()

        if attributes:
            self.write(f'<{element_name} {attributes}>',
                       indent=True,
                       blank=blank_before)
        else:
            self.write(f'<{element_name}>', indent=True, blank=blank_before)
        yield
        self.current_indent = starting_indent
        self.write(f'</{element_name}>', blank=blank)

    def figure(self, src, href='', caption='', alt='', blank=False, **attrs):
        with self.block('figure', blank=blank):
            with self.block('a', href=href or src):
                if alt:
                    self.write(f'<img src="{src}" alt="{alt}" />')
                else:
                    self.write(f'<img src="{src}" />')

            if caption:
                with self.block('figcaption'):
                    self.write(f'<p>{caption}</p>')


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
        html.write(
            '<meta name="viewport" content="width=device-width, initial-scale=1"/>'
        )
        html.write(f'<meta name="twitter:title" content="{page.title}"/>')
        html.write(
            f'<meta name="twitter:description" content="{page.description}"/>')
        html.write(f'<meta property="og:url" content="{page_url}"/>')
        html.write('<meta property="og:type" content="article"/>')
        html.write(f'<meta property="og:title" content="{page.title}"/>')
        html.write(
            f'<meta property="og:description" content="{page.description}"/>')
        if page.banner:
            banner = urllib.parse.urljoin(full_url.geturl(),
                                          f'/images/banners/{page.banner}')
            html.write(f'<meta name="image" content="{banner}"/>')
            html.write(f'<meta property="og:image" content="{banner}"/>')
        with html.indentation_reset():
            html.write('')

    html.write('<body>', indent=True, blank=True)

    html.comment('Page Header')
    with html.block('header', blank=True):
        html.write(f'<h1>{page.title}</h1>')
        html.write(f'<h2>{page.description}</h2>')

    html.write('<hr/>', blank=True)

    html.write('<!-- Site Navigation -->')
    with html.block('nav', blank=True):
        html.write('<a href="./index.html">index.html</a>')
        if page.filename != 'index.html':
            html.write('<span>/</span>')
            html.write(f'<span>{page.filename}</span>')
        # TODO: remove these classes - just target the elements and make
        # the markup more generic.
        html.write('<br class="show-on-mobile">')
        with html.block('span', _class='float-right-on-desktop'):
            for nav_page in nav_pages:
                html.write(f'<a href="./{nav_page}">{nav_page}</a>')

    html.write('<hr/>', blank=True)

    if page.banner:
        html.comment('Page Banner')
        html.figure(src=f'./images/banners/{page.banner}',
                    alt='banner',
                    blank=True)

    html.comment('Page Content')
    with html.block('article', blank=True, blank_before=True):
        with html.indentation_reset():
            html.write(content)

    html.write('<hr/>', blank=True)

    html.write('<!-- Page Footer -->')
    with html.block('footer', blank=True):
        html.write(f'<small>Built with Python {python_version}</small>')
        html.write(f'<small>© Copyright {copyright_year} {author}</small>')

    html.unindent()
    html.write('</body>', blank=True)

    html.comment(
        'No JavaScript, cookies, or tracking.  Just enjoy the reading!')
    html.write('</html>')

    return html.text


@contextlib.contextmanager
def write_page(directory: pathlib.Path, filename: str, overwrite_ok=False):
    """Writes a file to the webroot in the 'www/' subdirectory.

    Makes a really big deal if it sees that a file is already there,
    since that would mean you have two places of code writing to the
    same place.
    """

    target = directory / f'www/{filename}'

    if not overwrite_ok and target.exists():
        raise FileExistsError(f'{target.name} already exists in webroot!')

    with open(target, 'w') as f:
        yield f
