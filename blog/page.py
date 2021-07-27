import datetime
import functools
import logging
import os
import pathlib
import re
import sys

logger = logging.getLogger(__name__)


class Page:
    def __init__(self, source: pathlib.Path):
        self.source = source

    def __repr__(self):
        return f'<Page {self.source.name}>'

    def read(self):
        with open(self.source) as f:
            return f.read()

    @functools.cached_property
    def metadata(self):
        metadata, _ = extract_markdown_frontmatter(self.read())
        logger.debug('extracted metadata %s from %s', metadata, self)
        return metadata

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
        # TODO: get rid of frontmatter!
        _, body = extract_markdown_frontmatter(self.read())
        if self.is_markdown():  # TODO: get rid of markdown!
            try:
                import markdown
                return markdown.markdown(body)
            except ImportError:
                logger.fatal('markdown package must be installed!')
                sys.exit(1)
        else:
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

    return None, content
