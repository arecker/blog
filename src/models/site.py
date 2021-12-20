import datetime
import functools
import logging
import os

from src import macro, git, utils
from src.models.page import Page
from src.models.feed import Feed
from src.models.sitemap import Sitemap
from src.models.archive import Archive

logger = logging.getLogger(__name__)


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

        self._archive = kwargs.pop('archive', None)
        self._pages = kwargs.pop('pages', None)
        self._entries = kwargs.pop('entries', None)
        self._sitemap = kwargs.pop('sitemap', None)
        self._feed = kwargs.pop('feed', None)

    def __repr__(self):
        return f'<Site {utils.prettify_path(self.directory)}>'

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

    @property
    def archive(self):
        if not self._archive:
            self._archive = Archive(site=self)
        return self._archive

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
        return utils.paginate_list(filenames)

    @functools.cached_property
    def commit(self):
        return git.get_head_commit(self.directory)

    @functools.cached_property
    def is_entry_tagged(self):
        return git.head_is_entry_tagged(root_directory=self.directory)
