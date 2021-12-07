import collections
import datetime
import functools
import logging
import pathlib
import re
import subprocess

from src import macro, git
from src.pagination import paginate_list

logger = logging.getLogger(__name__)

Commit = collections.namedtuple('Commit',
                                ['short_hash', 'long_hash', 'summary'])


class Site:
    def __init__(self,
                 args=None,
                 timestamp=None,
                 entries=[],
                 pages=[],
                 directory=None,
                 feed=None,
                 sitemap=None):
        self.timestamp = timestamp or datetime.datetime.now()

        if entries:
            self._entries = entries

        if pages:
            self._pages = pages

        if directory:
            self.directory = pathlib.Path(directory).expanduser().absolute()

        if feed:
            self._feed = feed

        if sitemap:
            self._sitemap = sitemap

        if args:
            self.args = args
            self.directory = pathlib.Path(
                args.root_directory).expanduser().absolute()
            self.title = args.title
            self.subtitle = args.subtitle
            self.author = args.author
            self.email = args.email
            self.domain = args.domain
            self.protocol = args.protocol
            self.basepath = args.basepath

        self.expander = macro.Expander(site=self)

    @property
    def directory_pretty(self):
        home = pathlib.Path.home()
        return re.sub(f'^{home}/', '~/', str(self.directory))

    def __repr__(self):
        return f'<Site {self.directory_pretty}>'

    @property
    def uri(self):
        return f'{self.protocol}://{self.domain}{self.basepath}'

    def href(self, path):
        return self.uri + path

    @property
    def entries(self):
        if not hasattr(self, '_entries'):
            from src.models import Page
            sources = sorted(self.directory.glob('entries/*.html'),
                             reverse=True)
            self._entries = [
                Page(source=source, site=self) for source in sources
            ]

        return self._entries

    @property
    def pages(self):
        if not hasattr(self, '_pages'):
            from src.models import Page
            sources = sorted(self.directory.glob('pages/*.html'))
            self._pages = [
                Page(source=source, site=self) for source in sources
            ]

        return self._pages

    @property
    def feed(self):
        if not hasattr(self, '_feed'):
            from src.models import Feed
            self._feed = Feed(site=self)
        return self._feed

    @property
    def sitemap(self):
        if not hasattr(self, '_sitemap'):
            from src.models import Sitemap
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
    def pagination(self):
        filenames = [f.filename for f in reversed(self.entries)]
        return paginate_list(filenames)

    @functools.cached_property
    def commit(self):
        def shell_command(cmd):
            result = subprocess.run(cmd.split(' '), capture_output=True)
            return result.stdout.decode('UTF-8').strip()

        return Commit(
            short_hash=shell_command('git rev-parse --short HEAD'),
            long_hash=shell_command('git rev-parse HEAD'),
            summary=shell_command('git log -1 --pretty=format:%s HEAD'))

    @functools.cached_property
    def is_entry_tagged(self):
        return git.head_is_entry_tagged(root_directory=self.directory)

    @property
    def commit_url(self):
        return f'https://github.com/arecker/blog/commit/{self.commit.long_hash}'
