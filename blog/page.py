import datetime
import logging
import os
import pathlib
import re
import sys

logger = logging.getLogger(__name__)


class Page:
    def __init__(self, source):
        self.source = pathlib.Path(source)

    def __repr__(self):
        return f'<Page {self.source.name}>'

    def read(self):
        with open(self.source) as f:
            return f.read()

    @property
    def metadata(self):
        if getattr(self, '_metadata', None):
            return self._metadata

        legacy_metadata, rest = extract_markdown_frontmatter(self.read())
        metadata, rest = extract_metadata_from_comments(rest)
        self._metadata = legacy_metadata | metadata
        return self._metadata

    @property
    def date(self):
        if not self.is_entry():
            return None
        slug, _ = os.path.splitext(self.source.name)
        return datetime.datetime.strptime(slug, '%Y-%m-%d')

    @property
    def filename(self):
        slug, _ = os.path.splitext(self.source.name)
        return slug + '.html'

    @property
    def title(self):
        if self.is_entry():
            return self.date.strftime('%A, %B %-d %Y')
        else:
            return self.metadata['title']

    @property
    def description(self):
        if self.is_entry():
            return self.metadata['title']
        return self.metadata['description']

    @property
    def banner(self):
        return self.metadata.get('banner', None)

    @property
    def content(self):
        _, body = extract_markdown_frontmatter(self.read())

        if self.is_markdown():
            try:
                import markdown
                body = markdown.markdown(body)
            except ImportError:
                logger.fatal('markdown package must be installed!')
                sys.exit(1)

        _, body = extract_metadata_from_comments(body)
        return body

    def is_entry(self):
        return self.source.parent.name == 'entries'

    def is_markdown(self):
        _, ext = os.path.splitext(self.source.name)
        return ext in ['.md', '.markdown']


def extract_markdown_frontmatter(content: str) -> dict:
    r"""Extracts YAML frontmatter from a string, returning a dict form
    along with the rest of the string.

    >>> content = '---\na: 1\nb: 2\nc: do re mi\n---\nThis is a test.'
    >>> results = extract_markdown_frontmatter(content)
    >>> results[0]
    {'a': '1', 'b': '2', 'c': 'do re mi'}
    >>> results[1]
    'This is a test.'
    """

    r_frontmatter = re.compile(r'^---\n(.*?)\n---\n(.*)$', re.DOTALL)
    r_frontmatter_line = re.compile(r'^(?P<key>.*?):\W?(?P<value>.*)$',
                                    re.MULTILINE)

    if match := r_frontmatter.match(content):
        body, rest = match.group(1, 2)
        data = dict(r_frontmatter_line.findall(body))
        return data, rest

    return {}, content


def extract_metadata_from_comments(content):
    pattern = re.compile(
        r'^\s?<!--\s?meta:(?P<key>[A-za-z]+)\s?(?P<value>.*)\s?-->$')

    metadata, rest = [], []

    for line in content.splitlines():
        if match := pattern.match(line):
            metadata.append([i.strip() for i in match.groups()])
        else:
            rest.append(line)

    return dict(metadata), '\n'.join(rest)
