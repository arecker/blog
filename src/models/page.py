import datetime
import logging
import os
import pathlib
import re

from src import html

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
        """The web page file name without the file extension.

        >>> Page(source='pages/index.html').slug
        'index'
        """

        return os.path.splitext(self.source.name)[0]

    @property
    def filename(self):
        """The web page file name, as it exists in the public webroot.

        >>> Page(source='pages/index.md').filename
        'index.html'
        """

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
            return f'/images/banners/{self.banner}'
        return None

    @property
    def banner_absolute_url(self):
        if self.banner:
            return self.site.uri + f'images/banners/{self.banner}'
        return None

    @property
    def nav_index(self):
        try:
            return int(self.metadata['nav'])
        except (ValueError, KeyError):
            return None

    def render(self):
        root = html.root()

        head = html.build_page_head(page_filename=self.filename,
                                    page_title=self.title,
                                    page_description=self.description,
                                    page_banner_url=self.banner_absolute_url)
        root.append(head)

        body = html.body()

        header = html.build_page_header(title=self.title,
                                        description=self.description)
        body.append(header)

        body.append(html.divider())

        nav = html.build_page_nav(filename=self.filename,
                                  nav_pages=self.site.nav)
        body.append(nav)

        body.append(html.divider())

        if self.banner:
            banner = html.build_page_banner(self.banner_url)
            body.append(banner)

        article = html.build_page_article(raw_content=self.raw_content)
        body.append(article)

        if self.is_entry:
            pages = self.site.pagination[self.filename]
            pagination = html.build_page_pagination(
                next_page=pages.next, previous_page=pages.previous)
            body.append(pagination)

        body.append(html.divider())

        footer = html.build_page_footer(author=self.site.author,
                                        year=self.site.timestamp.year)
        body.append(footer)
        root.append(body)
        root = html.stringify_xml(root)

        if not self.is_entry:
            root = self.site.expander.expand(root)

        return f'<!doctype html>\n{root}'

    def build(self):
        with open(self.site.directory / self.target, 'w') as f:
            f.write(self.render())
