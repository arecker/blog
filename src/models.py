import datetime
import functools
import itertools
import logging
import os
import pathlib
import re

from src import macro, git, html, xml, pagination

logger = logging.getLogger(__name__)


class Page:
    def __init__(self, **kwargs):
        self.site = kwargs.pop('site', None)

        try:
            self.source = pathlib.Path(kwargs.pop('source'))
        except KeyError:
            self.source = None

        self._is_entry = kwargs.pop('is_entry', None)
        self._content = kwargs.pop('content', None)
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
            pattern = re.compile(
                r'^\s?<!--\s?meta:(?P<key>[A-za-z]+)\s?(?P<value>.*)\s?-->$',
                re.MULTILINE)
            values = [(k.strip(), v.strip())
                      for k, v in pattern.findall(self.content)]
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

    def banner_href(self, full=False):
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


class Archive:
    def __init__(self, site=None):
        self.site = site

    def __repr__(self):
        path = '/'.join([self.site.directory_pretty, 'entries/'])
        return f'<Archive {path}>'

    def list_years(self):
        years = [entry.date.year for entry in self.site.entries]
        return sorted(set(years), reverse=True)

    def list_months(self, year):
        entries = filter(lambda e: year == e.date.year, self.site.entries)
        months = [e.date.month for e in entries]
        return sorted(set(months), reverse=True)

    def list_entries(self, year, month):
        entries = filter(lambda e: year == e.date.year, self.site.entries)
        entries = filter(lambda e: month == e.date.month, entries)
        return sorted(entries, key=lambda e: e.date, reverse=True)


class Sitemap(Page):
    filename = 'sitemap.xml'

    def __init__(self, site):
        self.site = site

    def render(self):
        root = xml.new_sitemap()

        for element in xml.as_location_elements(locations=self.locations):
            root.append(element)

        return xml.stringify_xml(root)

    @property
    def locations(self):
        for page in itertools.chain(self.site.entries, self.site.pages):
            url = self.site.href(page.filename, full=True)
            if page.is_entry:
                yield url, page.date
            else:
                yield url, self.site.timestamp


class Feed(Page):
    filename = 'feed.xml'

    def __init__(self, site):
        self.site = site

    def render(self):
        feed = xml.new_feed(title=self.site.title,
                            subtitle=self.site.subtitle,
                            author=self.site.author,
                            email=self.site.email,
                            timestamp=self.site.latest.date,
                            feed_uri=self.site.href('feed.xml', full=True),
                            site_uri=self.site.href(full=True))

        for item in self.items():
            feed.append(item)

        return xml.stringify_xml(feed)

    def items(self):
        return map(xml.as_feed_entry, itertools.islice(self.site.entries, 30))


class Site:
    def __init__(self, **kwargs):
        self.author = kwargs.pop('author', None)
        self.basepath = kwargs.pop('basepath', '/')
        self.directory = kwargs.pop('directory', None)
        self.domain = kwargs.pop('domain', None)
        self.email = kwargs.pop('email', None)
        self.protocol = kwargs.pop('protocol', None)
        self.subtitle = kwargs.pop('subtitle', None)
        self.timestamp = kwargs.pop('timestamp', datetime.datetime.now())
        self.title = kwargs.pop('title', None)

        self._pages = kwargs.pop('pages', None)
        self._entries = kwargs.pop('entries', None)
        self._sitemap = kwargs.pop('sitemap', None)
        self._feed = kwargs.pop('feed', None)

    @property
    def directory_pretty(self):
        home = pathlib.Path.home()
        return re.sub(f'^{home}/', '~/', str(self.directory))

    def __repr__(self):
        return f'<Site {self.directory_pretty}>'

    def href(self, path='', full=False):
        """Render an path as an href.

        >>> Site().href('test.html')
        '/test.html'

        Will add a trailing slash if there is no file extension.

        >>> Site().href('something')
        '/something/'

        Will account for the site's basepath.

        >>> Site(basepath='/subpath/').href('another')
        '/subpath/another/'

        Can do full URI's as well.

        >>> Site(domain='test.com', protocol='http', basepath='/subdir/').href('test.html', full=True)
        'http://test.com/subdir/test.html'

        Calling no args just returns the site's basepath.

        >>> Site().href()
        '/'

        Calling with just full returns the site URI.

        >>> Site(domain='test.com', protocol='http').href(full=True)
        'http://test.com/'
        """
        if path.startswith('/'):
            path = path[1:]

        if path and not path.endswith('/') and not os.path.splitext(path)[1]:
            path = path + '/'

        if not (self.basepath.startswith('/') and self.basepath.endswith('/')):
            raise ValueError(
                f'basepath "{self.basepath}" should start and end with a slash!'
            )

        relative = self.basepath + path

        if full:
            return f'{self.protocol}://{self.domain}{relative}'
        else:
            return relative

    @property
    def entries(self):
        if not self._entries:
            sources = sorted(self.directory.glob('entries/*.html'),
                             reverse=True)
            self._entries = [
                Page(source=source, site=self) for source in sources
            ]

        return self._entries

    @property
    def pages(self):
        if not self._pages:
            sources = sorted(self.directory.glob('pages/*.html'))
            self._pages = [
                Page(source=source, site=self) for source in sources
            ]

        return self._pages

    @property
    def feed(self):
        if not self._feed:
            self._feed = Feed(site=self)
        return self._feed

    @property
    def sitemap(self):
        if not self._sitemap:
            self._sitemap = Sitemap(site=self)
        return self._sitemap

    @functools.cached_property
    def nav(self):
        pages = sorted(filter(lambda p: p.nav_index, self.pages),
                       key=lambda p: p.nav_index)
        return [p.filename for p in pages]

    @property
    def latest(self):
        return self.entries[0]

    @functools.cached_property
    def expander(self):
        e = macro.Expander(site=self)
        e.populate()
        return e

    @functools.cached_property
    def pagination(self):
        filenames = [f.filename for f in reversed(self.entries)]
        return pagination.paginate_list(filenames)

    @functools.cached_property
    def commit(self):
        return git.get_head_commit(self.directory)

    @functools.cached_property
    def is_entry_tagged(self):
        return git.head_is_entry_tagged(root_directory=self.directory)
