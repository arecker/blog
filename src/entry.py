import collections
import datetime
import pathlib
import re


Entry = collections.namedtuple('Entry', [
    'filename',
    'banner',
    'title',
    'description',
    'date',
    'content',
])


def load_entries(entries_dir='./entries') -> list[Entry]:
    entries = []

    for p in pathlib.Path(entries_dir).glob('*.html'):
        kwargs = {}
        kwargs['filename'] = p.name

        # parse date
        kwargs['date'] = datetime.datetime.strptime(p.stem, '%Y-%m-%d')

        # set title
        kwargs['title'] = kwargs['date'].strftime('%A, %B %-d %Y')

        with p.open() as f:
            content = f.read()
            kwargs['content'] = content

        # parse metadata
        metadata = re.compile(
            r'^\s?<!--\s?meta:(?P<key>[A-za-z]+)\s?(?P<value>.*)\s?-->$',
            re.MULTILINE)
        metadata = [(k, v) for k, v in metadata.findall(content)]
        metadata = dict([(k.strip(), v.strip()) for k, v in metadata])

        kwargs['banner'] = metadata.get('banner')
        kwargs['description'] = metadata['title']

        entries.append(Entry(**kwargs))

    return sorted(entries, key=lambda e: e.date, reverse=True)


def parse_metadata(content: str) -> dict:
    metadata = re.compile(
        r'^\s?<!--\s?meta:(?P<key>[A-za-z]+)\s?(?P<value>.*)\s?-->$',
        re.MULTILINE)
    metadata = [(k, v) for k, v in metadata.findall(content)]
    metadata = dict([(k.strip(), v.strip()) for k, v in metadata])
    return metadata
