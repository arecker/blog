import collections
import datetime
import pathlib
import re


Page = collections.namedtuple('Page', [
    'path',
    'filename',
    'title',
    'description',
    'banner',
    'date',
    'next',
    'previous',
])


def load_pages(pages_dir='./pages'):
    pages = []

    for p in pathlib.Path(pages_dir).glob('*.*'):
        kwargs = {}

        kwargs['path'] = p

        if p.name.endswith('.j2'):
            kwargs['filename'] = p.name[:-3]
        else:
            kwargs['filename'] = p.name

        with p.open() as f:
            content = f.read()

        # date not supported on pages for now
        kwargs['date'] = None

        # get the rest from the metadata
        metadata = parse_metadata(content)
        kwargs['title'] = metadata['title']
        kwargs['description'] = metadata.get('description')
        kwargs['banner'] = metadata.get('banner')
        kwargs['next'] = metadata.get('next')
        kwargs['previous'] = metadata.get('previous')
        pages.append(Page(**kwargs))

    return sorted(pages, key=lambda p: p.filename)


def load_entries(entries_dir='./entries') -> list[Page]:
    entries = []

    entry_paths = list(sorted(pathlib.Path(entries_dir).glob('*.html')))

    # get pagination map
    pagination = paginate_entries(entry_paths)

    for p in entry_paths:
        kwargs = {}
        kwargs['path'] = p
        kwargs['filename'] = p.name

        # parse date
        kwargs['date'] = datetime.datetime.strptime(p.stem, '%Y-%m-%d')

        # set title
        kwargs['title'] = kwargs['date'].strftime('%A, %B %-d %Y')

        with p.open() as f:
            content = f.read()

        # get the rest from metadata
        metadata = parse_metadata(content)
        kwargs['banner'] = metadata.get('banner')
        kwargs['description'] = metadata['title']

        # check pagination map
        kwargs['next'] = pagination[p.name].next
        kwargs['previous'] = pagination[p.name].previous

        entries.append(Page(**kwargs))

    # sort latest first
    return sorted(entries, reverse=True)


Pagination = collections.namedtuple('Pagination', ['next', 'previous'])


def paginate_entries(files=[]):
    pagination = {}

    for i, this_file in enumerate(files):
        kwargs = {}

        if i > 0:
            kwargs['previous'] = files[i - 1].name
        else:
            kwargs['previous'] = None

        try:
            kwargs['next'] = files[i + 1].name
        except IndexError:
            kwargs['next'] = None

        pagination[this_file.name] = Pagination(**kwargs)

    return pagination


def parse_metadata(content: str) -> dict:
    metadata = re.compile(
        r'^\s?<!--\s?meta:(?P<key>[A-za-z]+)\s?(?P<value>.*)\s?-->$',
        re.MULTILINE)
    metadata = [(k, v) for k, v in metadata.findall(content)]
    metadata = dict([(k.strip(), v.strip()) for k, v in metadata])
    return metadata
