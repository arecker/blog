"""build website pages"""

from urllib.parse import urljoin
import datetime
import logging
import os
import pathlib
import re

from .. import utils, html
from ..utils import ROOT_DIR

logger = logging.getLogger(__name__)


# TODO: move this function somewhere else
def build_nav_list():
    pages = utils.ROOT_DIR.glob('pages/*.html')
    pages = [Page(source=source) for source in pages]
    pages = filter(lambda p: p.nav_index, pages)
    pages = sorted(pages, key=lambda p: p.nav_index)

    return ['entries.html'] + [p.filename for p in pages]


class PageMetadata:
    """Mixin for Page Metadata

    Helps the page parse its own metadata either from HTML comments...

    >>> html = '<!-- meta:title A Tale of Two Cities -->'
    >>> PageMetadata(content=html).metadata()
    {'title': 'A Tale of Two Cities'}

    ...or from kwargs.

    >>> PageMetadata(metadata={'anything': 'Hello!'}).metadata()
    {'anything': 'Hello!'}
    """
    def __init__(self, content='', metadata={}, **kwargs):
        super()
        self._content = content
        self._metadata = metadata

    def metadata(self) -> dict:
        if self._metadata:
            return self._metadata

        if self._content:
            return self.metadata_parse_html(self._content)

        content = self.read()
        return self.metadata_parse_html(content)

    def metadata_parse_html(self, content):
        """Parse metadata from magic HTML comments.

        >>> html = '<!-- meta:title A Tale of Two Cities -->'
        >>> PageMetadata().metadata_parse_html(html)
        {'title': 'A Tale of Two Cities'}
        """
        pattern = re.compile(
            r'^\s?<!--\s?meta:(?P<key>[A-za-z]+)\s?(?P<value>.*)\s?-->$',
            re.MULTILINE)
        values = [(k.strip(), v.strip()) for k, v in pattern.findall(content)]
        return dict(values)


class Page(PageMetadata):
    def __init__(self, **kwargs):
        self.site = kwargs.pop('site', None)

        try:
            self.source = pathlib.Path(kwargs.pop('source'))
        except KeyError:
            self.source = None

        self._banner = kwargs.pop('banner', None)
        self._content = kwargs.pop('content', None)
        self._description = kwargs.pop('description', None)
        self._filename = kwargs.pop('filename', None)
        self._is_entry = kwargs.pop('is_entry', None)
        self._metadata = kwargs.pop('metadata', None)
        self._title = kwargs.pop('title', None)

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
        if self._filename:
            return self._filename
        else:
            return self.slug + '.html'

    def href(self, full=False):
        return self.site.href(self.filename, full=full)

    @property
    def target(self):
        """Write destination of the web page file, relative to the
        site root directory.

        >>> Page(source='pages/test.html').target
        'www/test.html'
        """

        return f'www/{self.filename}'

    @property
    def is_entry(self):
        """True if the source in the entries folder and the page
        should be treated like an entry.

        >>> Page(source='entries/test.html').is_entry
        True

        >>> Page(source='pages/test.html').is_entry
        False

        You can also override this when making a page for testing.

        >>> Page(is_entry=False).is_entry
        False
        """
        if self._is_entry is None:
            return self.source.parent.name == 'entries'
        else:
            return self._is_entry

    @property
    def content(self):
        if not self._content:
            with open(self.source, 'r') as f:
                self._content = f.read()
        return self._content

    @property
    def date(self):
        if not self.is_entry:
            return None
        else:
            return datetime.datetime.strptime(self.slug, '%Y-%m-%d')

    @property
    def title(self):
        if self._title:
            return self._title
        elif self.is_entry:
            return self.date.strftime('%A, %B %-d %Y')
        else:
            return self.metadata()['title']

    @property
    def description(self):
        if self._description:
            return self._description

        metadata = self.metadata()
        if self.is_entry:
            return metadata['title']
        else:
            return metadata['description']

    @property
    def banner(self):
        if not self._banner:
            metadata = self.metadata()
            self._banner = metadata.get('banner', None)
        return self._banner

    @property
    def nav_index(self):
        try:
            metadata = self.metadata()
            return int(metadata['nav'])
        except (ValueError, KeyError):
            return None

    def render(self, author='', year='', full_url='', nav_pages=[]):
        assert all([author, year, full_url, nav_pages]), 'missing some args!'

        root = html.root()

        banner_url = urljoin(
            f'{full_url.scheme}://{full_url.netloc}{full_url.path}',
            f'images/banners/{self.banner}')

        head = html.build_page_head(page_filename=self.filename,
                                    page_title=self.title,
                                    page_description=self.description,
                                    page_banner_url=banner_url)
        root.append(head)

        body = html.body()

        header = html.build_page_header(title=self.title,
                                        description=self.description)
        body.append(header)

        body.append(html.divider())

        nav = html.build_site_nav(filename=self.filename, nav_pages=nav_pages)
        body.append(nav)

        body.append(html.divider())

        if self.banner:
            banner_url = f'./images/banners/{self.banner}'
            banner = html.build_page_banner(banner_url)
            body.append(banner)

        article = html.build_page_article(raw_content=self.content)
        body.append(article)

        if self.is_entry:
            pages = self.site.pagination[self.filename]
            pagination = html.build_page_pagination(
                next_page=pages.next, previous_page=pages.previous)
            body.append(pagination)

        body.append(html.divider())

        footer = html.build_page_footer(author=author, year=year)
        body.append(footer)
        root.append(body)
        root = html.stringify_xml(root)

        if not self.is_entry:
            root = self.site.expander.expand(root)

        return f'<!doctype html>\n{root}'

    def read(self):
        """Returns the content of the pages off the filesystem."""

        with open(self.source, 'r') as f:
            return f.read()

    def build(self, **kwargs):
        with open(utils.ROOT_DIR / self.target, 'w') as f:
            f.write(self.render(**kwargs))


def register(parser):
    return parser


def main(args):
    pages = sorted(ROOT_DIR.glob('pages/*.html'))

    # TODO: remove once macro library is gone
    from ..models import Site
    site = Site(**vars(args))

    pages = [Page(source=source, site=site) for source in pages]

    nav_pages = build_nav_list()

    total = len(pages)
    for i, page in enumerate(pages):
        page.build(author=args.author,
                   year=args.year,
                   full_url=args.full_url,
                   nav_pages=nav_pages)
        logger.info('generated %s (%d/%d pages)', page.target, i + 1, total)
