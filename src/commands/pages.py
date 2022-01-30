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

    Helps the page parse its own metadata either from HTML comments.

    >>> o = PageMetadata()
    >>> o._content = '<!-- meta:title A Tale of Two Cities -->'
    >>> o.metadata()
    {'title': 'A Tale of Two Cities'}

    Set `_metadata` to override the results.

    >>> o._metadata = {'anything': 'Hello!'}
    >>> o.metadata()
    {'anything': 'Hello!'}
    """
    def metadata(self) -> dict:
        if data := getattr(self, '_metadata', None):
            return data

        if data := getattr(self, '_content', None):
            content = data
        else:
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


class PageBanner:
    """Mixin Page Banner

    Helps the page find and render its banner.

    >>> o = PageBanner()
    >>> o._banner = 'test.jpg'
    >>> o.banner_filename()
    'test.jpg'

    Can render relative URL...

    >>> o = PageBanner()
    >>> o._banner = 'test.jpg'
    >>> o.banner_href()
    './images/banners/test.jpg'

    ... or a full url, if the full_url param is provided.

    >>> from urllib.parse import urlparse
    >>> full_url = urlparse('https://www.yoursite.biz')
    >>> o = PageBanner()
    >>> o._banner = 'test.jpg'
    >>> o.banner_href(full_url=full_url)
    'https://www.yoursite.biz/images/banners/test.jpg'
    """
    def banner_filename(self):
        """Return the banner filename.

        If none was given in kwargs, attempt to access the Page's
        metadata.
        """
        if banner := getattr(self, '_banner', None):
            return banner

        metadata = self.metadata()
        return metadata.get('banner')

    def banner_href(self, full_url=None):
        filename = self.banner_filename()

        if not filename:
            return None

        if not full_url:
            return f'./images/banners/{filename}'

        return urljoin(f'{full_url.scheme}://{full_url.netloc}{full_url.path}',
                       f'images/banners/{filename}')


class PageMarkup:
    """Mixin for Page Markup.

    Helps the page generate HTML.
    """
    def html_head(self,
                  filename='',
                  title='',
                  description='',
                  full_url='',
                  banner_url=''):
        """Generates HTML <head> section.

        :param str filename: The name of the rendered file in the webroot        

        >>> o = PageMarkup()
        >>> kwargs = {'title': 'Test', 'description': 'A Test Page'}
        >>> kwargs.update({'full_url': 'test.html', 'banner_url': 'test.jpg'})
        >>> from ..html import stringify_xml
        >>> xml = o.html_head(**kwargs)
        >>> print(stringify_xml(xml))
        <head>
          <title>Test</title>
          <link rel="shortcut icon" type="image/x-icon" href="./favicon.ico">
          <link href="./assets/site.css" rel="stylesheet">
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <meta name="twitter:title" content="Test">
          <meta name="twitter:description" content="A Test Page">
          <meta name="image" content="test.jpg">
          <meta property="og:url" content="/">
          <meta property="og:type" content="article">
          <meta property="og:title" content="Test">
          <meta property="og:description" content="A Test Page">
          <meta property="og:image" content="test.jpg">
        </head>
        """
        kwargs = {
            'page_filename': filename,
            'page_title': title,
            'page_description': description,
            'page_banner_url': banner_url,
        }

        return html.build_page_head(**kwargs)

    def html_body(self,
                  title='',
                  description='',
                  filename='',
                  nav_pages=[],
                  banner_href='',
                  content=''):
        """Generates HTML <body>"""

        body = html.body()
        header = html.build_page_header(title=title, description=description)
        body.append(header)
        body.append(html.divider())
        nav = html.build_site_nav(filename=filename, nav_pages=nav_pages)
        body.append(nav)

        body.append(html.divider())

        if banner_href:
            banner = html.build_page_banner(banner_href)
            body.append(banner)

        article = html.build_page_article(raw_content=content)
        body.append(article)

        return body


class Page(PageMetadata, PageBanner, PageMarkup):
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
    def content(self):
        if not self._content:
            with open(self.source, 'r') as f:
                self._content = f.read()
        return self._content

    @property
    def title(self):
        if self._title:
            return self._title
        else:
            return self.metadata()['title']

    @property
    def description(self):
        if self._description:
            return self._description

        metadata = self.metadata()
        return metadata['description']

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

        head = self.html_head(filename=self.filename,
                              title=self.title,
                              description=self.description,
                              full_url=full_url,
                              banner_url=self.banner_href(full_url=full_url))
        root.append(head)

        body = self.html_body(title=self.title,
                              description=self.description,
                              filename=self.filename,
                              nav_pages=nav_pages,
                              banner_href=self.banner_href(),
                              content=self.read())

        body.append(html.divider())
        footer = html.build_page_footer(author=author, year=year)
        body.append(footer)

        root.append(body)
        root = html.stringify_xml(root)

        # TODO: rewrite the index page as a separate Page type so we
        # can get rid of this expander
        root = self.site.expander.expand(root)

        return f'<!doctype html>\n{root}'

    def read(self):
        """Returns the content of the pages off the filesystem."""

        # TODO: override read() in archive instead
        if content := getattr(self, '_content', None):
            return content

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
