import collections
import pathlib
import re


Page = collections.namedtuple('Page', [
    'filename',
    'title',
    'description',
    'template_name',
    'banner',
])


def load_pages(pages_dir='./pages'):
    pages = []

    for p in pathlib.Path(pages_dir).glob('*.html.j2'):
        kwargs = {}

        kwargs['filename'] = p.name[:-3]
        kwargs['template_name'] = p.name

        with p.open() as f:
            content = f.read()

        # parse metadata
        metadata = parse_metadata(content)
        kwargs['title'] = metadata['title']
        kwargs['description'] = metadata.get('description')
        kwargs['banner'] = metadata.get('banner')
        pages.append(Page(**kwargs))

    return sorted(pages, key=lambda p: p.filename)


def parse_metadata(content: str) -> dict:
    metadata = re.compile(
        r'^\s?<!--\s?meta:(?P<key>[A-za-z]+)\s?(?P<value>.*)\s?-->$',
        re.MULTILINE)
    metadata = [(k, v) for k, v in metadata.findall(content)]
    metadata = dict([(k.strip(), v.strip()) for k, v in metadata])
    return metadata
