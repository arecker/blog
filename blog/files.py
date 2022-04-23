import collections
import datetime
import logging
import pathlib
import re
import urllib.parse

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
