import datetime
import os
import pathlib
from xml.etree import ElementTree as ET

from . import logger, markdown


class Page:
    def __init__(self, source, metadata={}):
        self.source = pathlib.Path(source)

        self._metadata = metadata

    @property
    def is_entry(self) -> bool:
        """Returns True if the source file is an entry.

        >>> Page('entries/test.md').is_entry
        True
        """
        return self.source.parent.name == 'entries'

    @property
    def is_markdown(self) -> bool:
        """Returns True if the source file is markdown.

        >>> Page('test.html').is_markdown
        False
        >>> Page('test.md').is_markdown
        True
        """
        _, ext = os.path.splitext(self.source)
        return ext == '.md'

    @property
    def filename(self):
        """Filename of the rendered page target.

        >>> Page('pages/test.html').filename
        'test.html'
        >>> Page('something/something.md').filename
        'something.html'
        """

        basename = os.path.basename(self.source)
        name, _ = os.path.splitext(basename)
        return name + '.html'

    def read(self):
        """Read raw contents of source file."""

        logger.debug('opening %s for read', self.source)

        with open(self.source, 'r') as f:
            return f.read()

    @property
    def metadata(self):
        """Page metadata.

        If the page is markdown, this is extracted from page frontmatter.
        """
        if self._metadata:
            return self._metadata

        # For now, both HTML and Markdown files use frontmatter.
        data, _ = markdown.extract_markdown_frontmatter(self.read())
        logger.debug('extracted frontmatter %s from %s', data, self.source)
        return data

    @property
    def title(self):
        """Page title.

        If the page is an entry, this will be based on the date.

        >>> Page('entries/2020-01-01.html').title
        'Wednesday, January 1 2020'

        Otherwise, the title is extracted from the metadata field
        "title".

        >>> Page('index.html', {'title': 'Home'}).title
        'Home'
        """
        if not self.is_entry:
            return self.metadata['title']

        return self.date.strftime('%A, %B %-d %Y')

    @property
    def description(self):
        """The page description.

        If the page is an entry, this will map to the 'title' metadata
        field.

        >>> Page('entries/test.html', {'title': 'my big dumb mouth'}).description
        'my big dumb mouth'

        Otherwise, this will map to the 'description' metadata field.

        >>> Page('index.html', {'description': 'The Index'}).description
        'The Index'
        """
        if self.is_entry:
            return self.metadata['title']
        return self.metadata['description']

    @property
    def banner(self) -> str:
        """Filename of the page banner.

        >>> metadata = {'title': 'Test', 'banner': 'test.jpg'}
        >>> Page('page.html', metadata).banner
        'test.jpg'

        None if there is no banner set in metadata.

        >>> Page('page.html', metadata={'title': 'Test'}).banner is None
        True
        """
        return self.metadata.get('banner', None)

    @property
    def date(self) -> datetime.datetime:
        """Entry date based on the filename.

        >>> Page('entries/2020-01-01.html').date
        datetime.datetime(2020, 1, 1, 0, 0)

        Returns None if not an entry.

        >>> Page('test.html').date is None
        True
        """
        if not self.is_entry:
            return None

        slug, _ = os.path.splitext(self.filename)
        return datetime.datetime.strptime(slug, '%Y-%m-%d')

    def html_head_title(self) -> ET.Element:
        """Render page title tag.

        >>> metadata = {'title': 'One Fat Summer', 'description': 'A Book Report'}
        >>> element = Page('page.html', metadata).html_head_title()
        >>> ET.indent(element)
        >>> ET.dump(element)
        <title>One Fat Summer | A Book Report</title>
        """

        tree = ET.TreeBuilder()
        tree.start('title', {})
        tree.data(f'{self.title} | {self.description}')
        tree.end('title')
        return tree.close()

    def html_meta_twitter(self) -> [ET.Element]:
        """Renders property="twitter:..." meta elements.

        >>> metadata = {'title': 'Test', 'description': 'A Test'}
        >>> elements = Page('page.html', metadata).html_meta_twitter()
        >>> _ = [ET.dump(element) for element in elements]
        <meta name="twitter:title" content="Test" />
        <meta name="twitter:description" content="A Test" />

        If there is a banner, that will be added as well.

        >>> metadata = {'title': 'Test', 'description': 'A Test', 'banner': 'test.jpg'}
        >>> elements = Page('page.html', metadata).html_meta_twitter()
        >>> _ = [ET.dump(element) for element in elements]
        <meta name="twitter:title" content="Test" />
        <meta name="twitter:description" content="A Test" />
        <meta name="twitter:image" content="https://www.alexrecker.com/images/banners/test.jpg" />
        """

        tags = {
            'title': self.title,
            'description': self.description,
        }

        if self.banner:
            tags[
                'image'] = f'https://www.alexrecker.com/images/banners/{self.banner}'

        elements = []

        for k, v in tags.items():
            attributes = {'name': f'twitter:{k}', 'content': v}
            el = ET.Element('meta', **attributes)
            elements.append(el)

        return elements

    def html_meta_og(self) -> [ET.Element]:
        """Renders property="og:..." meta elements.

        >>> metadata = {'title': 'Test', 'description': 'A Test'}
        >>> elements = Page('page.html', metadata).html_meta_og()
        >>> _ = [ET.dump(element) for element in elements]
        <meta property="og:url" content="/page.html" />
        <meta property="og:type" content="article" />
        <meta property="og:title" content="Test" />
        <meta property="og:description" content="A Test" />

        If there is a banner, that will be added as well.

        >>> metadata = {'title': 'Test', 'description': 'A Test', 'banner': 'test.jpg'}
        >>> elements = Page('page.html', metadata).html_meta_og()
        >>> _ = [ET.dump(element) for element in elements]
        <meta property="og:url" content="/page.html" />
        <meta property="og:type" content="article" />
        <meta property="og:title" content="Test" />
        <meta property="og:description" content="A Test" />
        <meta property="og:image" content="/images/banners/test.jpg" />
        """

        tags = {
            'url': f'/{self.filename}',
            'type': 'article',
            'title': self.title,
            'description': self.description,
        }

        if self.banner:
            tags['image'] = f'/images/banners/{self.banner}'

        elements = []

        for k, v in tags.items():
            attributes = {'property': f'og:{k}', 'content': v}
            el = ET.Element('meta', **attributes)
            elements.append(el)

        return elements

    def html_header(self):
        """Renders the HTML page header, based on the page title and
        description.

        >>> metadata = {'title': 'One Fat Summer', 'description': 'A Book Report'}
        >>> element = Page('page.html', metadata).html_header()
        >>> ET.indent(element)
        >>> ET.dump(element)
        <header>
          <h1>One Fat Summer</h1>
          <h2>A Book Report</h2>
        </header>
        """

        tree = ET.TreeBuilder()
        tree.start('header', {})
        tree.start('h1', {})
        tree.data(self.title)
        tree.end('h1')
        tree.start('h2', {})
        tree.data(self.description)
        tree.end('h2')
        tree.end('header')
        return tree.close()

    def html_breadcrumbs(self) -> [ET.Element]:
        """Renders breadcrumb elements for the page.

        >>> elements = Page('page.html', {}).html_breadcrumbs()
        >>> _ = [ET.dump(element) for element in elements]
        <a href="/">index.html</a>
        <span>/</span>
        <span>page.html</span>

        If the page is named "index.html", then just the homepage link
        is returned.

        >>> elements = Page('index.html', {}).html_breadcrumbs()
        >>> _ = [ET.dump(element) for element in elements]
        <a href="/">index.html</a>
        """

        elements = []

        # home link
        home = ET.Element('a', href='/')
        home.text = 'index.html'
        elements.append(home)

        if self.filename == 'index.html':
            return elements

        divider = ET.Element('span')
        divider.text = '/'
        elements.append(divider)

        page = ET.Element('span')
        page.text = self.filename
        elements.append(page)

        return elements

    def html_head(self) -> ET.Element:
        """Renders HTML head"""

        head = ET.Element('head')

        # title tag
        head.append(self.html_head_title())

        #link
        head.append(
            ET.Element('link',
                       rel='shortcut icon',
                       type='image/x-icon',
                       href='/favicon.ico'))
        head.append(
            ET.Element('link', href='/assets/site.css', rel='stylesheet'))

        # meta
        head.append(ET.Element('meta', charset='UTF-8'))
        head.append(
            ET.Element('meta',
                       name='viewport',
                       content='width=device-width, initial-scale=1'))

        # meta:twitter
        for element in self.html_meta_twitter():
            head.append(element)

        # meta:og
        for element in self.html_meta_og():
            head.append(element)

        return head

    def html_site_navigation(self, pages: list) -> ET.Element:
        """Renders site navigation

        >>> pages = ['a.html', 'b.html', 'c.html']
        >>> element = Page('page.html', {}).html_site_navigation(pages)
        >>> ET.indent(element)
        >>> ET.dump(element)
        <span class="float-right-on-desktop">
          <a href="/a.html">a.html</a>
          <a href="/b.html">b.html</a>
          <a href="/c.html">c.html</a>
        </span>
        """

        tree = ET.TreeBuilder()

        # TODO: another class to get rid of
        tree.start('span', {'class': 'float-right-on-desktop'})

        for page in pages:
            tree.start('a', {'href': f'/{page}'})
            tree.data(page)
            tree.end('a')

        tree.end('span')
        return tree.close()

    def html_nav(self, nav_pages=[]):
        """Render HTMl nav."""

        nav = ET.Element('nav')

        for element in self.html_breadcrumbs():
            nav.append(element)

        # TODO: get rid of CSS class
        nav.append(ET.Element('br', attrib={'class': 'show-on-mobile'}))

        # site navigation
        nav.append(self.html_site_navigation(nav_pages))

        return nav

    def html_body(self, nav_pages=[]):
        """Renders HTML body"""

        body = ET.Element('body')
        body.append(self.html_header())
        body.append(ET.Element('hr'))
        body.append(self.html_nav(nav_pages=nav_pages))

        return body

    def render(self, nav_pages=[]):
        """Render a page as an HTML string."""

        html = ET.Element('html', lang='en')
        html.append(self.html_head())
        html.append(self.html_body(nav_pages=nav_pages))

        ET.indent(html)
        document = ET.tostring(html).decode('UTF-8')

        return f'<!DOCTYPE html>\n{document}'
