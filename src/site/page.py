import datetime
import functools
import logging
import os
import pathlib
import re

from . import Document

logger = logging.getLogger(__name__)


class Page:
    def __init__(self, source=None, metadata={}, is_entry=None):
        self.source = pathlib.Path(source)
        if metadata:
            self._metadata = metadata
        if is_entry is not None:
            self._is_entry = is_entry

    def __repr__(self):
        return f'<Page {self.filename}>'

    @property
    def slug(self):
        return os.path.splitext(self.source.name)[0]

    @property
    def filename(self):
        return self.slug + '.html'

    @property
    def target(self):
        return f'www/{self.filename}'

    @property
    def is_entry(self):
        if not hasattr(self, '_is_entry'):
            return self.source.parent.name == 'entries'
        return self._is_entry

    @property
    def raw_content(self):
        with open(self.source, 'r') as f:
            return f.read()

    @property
    def metadata(self) -> dict:
        if not hasattr(self, '_metadata'):
            pattern = re.compile(
                r'^\s?<!--\s?meta:(?P<key>[A-za-z]+)\s?(?P<value>.*)\s?-->$',
                re.MULTILINE)
            values = [(k.strip(), v.strip())
                      for k, v in pattern.findall(self.raw_content)]
            self._metadata = dict(values)

        return self._metadata

    @property
    def date(self):
        if not self.is_entry:
            return None
        else:
            return datetime.datetime.strptime(self.slug, '%Y-%m-%d')

    @property
    def title(self):
        if self.is_entry:
            return self.date.strftime('%A, %B %-d %Y')
        else:
            return self.metadata['title']

    @property
    def description(self):
        if self.is_entry:
            return self.metadata['title']
        return self.metadata['description']

    @property
    def banner(self):
        return self.metadata.get('banner', None)

    @property
    def nav_index(self):
        try:
            return int(self.metadata['nav'])
        except (ValueError, KeyError):
            return None

    def render(self, site):
        document = Document(site=site, page=self)
        return document.render()

    def build(self, site):
        rendered = self.render(site)

        # expand macros in the page
        rendered = site.expander.expand(rendered)

        with open(site.directory / self.target, 'w') as f:
            f.write(rendered)
