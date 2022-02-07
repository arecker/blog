"""Some random functions."""

import collections
import datetime
import logging
import pathlib
import re

ROOT_DIR = pathlib.Path(__file__).parent.parent
logger = logging.getLogger(__name__)


def parse_html_metadata_comments(content):
    """Parse metadata from magic HTML comments.

    >>> parse_html_metadata_comments('<!-- meta:title A Tale of Two Cities -->')
    {'title': 'A Tale of Two Cities'}
    """

    pattern = re.compile(
        r'^\s?<!--\s?meta:(?P<key>[A-za-z]+)\s?(?P<value>.*)\s?-->$',
        re.MULTILINE)
    values = [(k.strip(), v.strip()) for k, v in pattern.findall(content)]
    return dict(values)


Entry = collections.namedtuple(
    'Entry', [
        'banner',
        'date',
        'description',
        'filename',
        'page_next',
        'page_previous',
        'source',
        'title',
    ]
)


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
        kwargs['banner'] = metadata.get('banner') # banner is optional
        kwargs['description'] = metadata['title'] # title is required

        # Set the pagination
        pagination = pages[source.name]
        kwargs['page_next'] = pagination.next
        kwargs['page_previous'] = pagination.previous

        entries.append(Entry(**kwargs))

    logger.info('parsed %d entries from %s', len(entries), prettify_path(entries_dir))
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


def month_name(month_int: int) -> str:
    """Return a month name for the integer.

    >>> month_name(6)
    'June'

    >>> month_name(1)
    'January'
    """

    date = datetime.datetime.strptime(str(month_int), '%m')
    return date.strftime('%B')
