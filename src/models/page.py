import datetime
import logging
import os
import pathlib
import re

logger = logging.getLogger(__name__)


class Page:
    def __init__(self,
                 source=None,
                 site=None,
                 raw_content=None,
                 metadata={},
                 is_entry=None):
        self.source = pathlib.Path(source)
        self.site = site
        if metadata:
            self._metadata = metadata
        if is_entry is not None:
            self._is_entry = is_entry
        if raw_content:
            self._raw_content = raw_content

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
        if not hasattr(self, '_raw_content'):
            with open(self.source, 'r') as f:
                self._raw_content = f.read()
        return self._raw_content

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
    def banner_url(self):
        if self.banner:
            return self.site.uri + f'images/banners/{self.banner}'
        return None

    @property
    def nav_index(self):
        try:
            return int(self.metadata['nav'])
        except (ValueError, KeyError):
            return None

    @property
    def meta_og_attrs(self):
        tags = {
            'url': f'/{self.filename}',
            'type': 'article',
            'title': self.title,
            'description': self.description,
        }

        if image := self.banner_url:
            tags['image'] = image

        return tags

    @property
    def meta_twitter_attrs(self):
        tags = {
            'twitter:title': self.title,
            'twitter:description': self.description,
        }

        if image := self.banner_url:
            tags['image'] = image

        return tags

    def render(self, site):
        from src.models import Document
        document = Document(site=site, page=self)
        return document.render()

    def build(self, site):
        rendered = self.render(site)

        if not self.is_entry:
            # expand macros in page
            rendered = site.expander.expand(rendered)

        with open(site.directory / self.target, 'w') as f:
            f.write(rendered)
