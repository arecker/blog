import datetime
import os
import pathlib

from blog import html, utils


class Page:
    def __init__(self, **kwargs):
        self.site = kwargs.pop('site', None)

        try:
            self.source = pathlib.Path(kwargs.pop('source'))
        except KeyError:
            self.source = None

        self._banner = kwargs.pop('banner', None)
        self._content = kwargs.pop('content', None)
        self._filename = kwargs.pop('filename', None)
        self._is_entry = kwargs.pop('is_entry', None)
        self._metadata = kwargs.pop('metadata', None)

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
    def metadata(self) -> dict:
        if self._metadata is None:
            self._metadata = utils.parse_html_metadata_comments(self.content)

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
        if not self._banner:
            self._banner = self.metadata.get('banner', None)
        return self._banner

    def banner_href(self, full=False):
        """Render the href of the page's banner image.
        >>> from blog.models import Site
        >>> Page(banner='test.jpg', site=Site()).banner_href()
        '/images/banners/test.jpg'

        Use full to render the full URI.

        >>> Page(banner='test.jpg', site=Site(protocol='http', domain='test.com')).banner_href(full=True)
        'http://test.com/images/banners/test.jpg'

        Returns None if the page doesn't have a banner.

        >>> Page(metadata={}).banner_href() is None
        True
        """

        if self.banner:
            return self.site.href(f'/images/banners/{self.banner}', full=full)

    @property
    def nav_index(self):
        try:
            return int(self.metadata['nav'])
        except (ValueError, KeyError):
            return None

    def render(self):
        root = html.root()

        head = html.build_page_head(
            page_filename=self.filename,
            page_title=self.title,
            page_description=self.description,
            page_banner_url=self.banner_href(full=True))
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
            banner = html.build_page_banner(self.banner_href())
            body.append(banner)

        article = html.build_page_article(raw_content=self.content)
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
