import collections
import datetime
import functools
import itertools
import logging
import os
import pathlib
import re
import subprocess

from . import Page, Feed, Sitemap
from .. import git, netlify

logger = logging.getLogger(__name__)

Pagination = collections.namedtuple('Pagination', ['next', 'previous'])
Commit = collections.namedtuple('Commit',
                                ['short_hash', 'long_hash', 'summary'])


class Site:
    def __init__(self, args):
        self.directory = pathlib.Path(args.root_directory).absolute()
        self.timestamp = datetime.datetime.now()

        self.title = args.title
        self.subtitle = args.subtitle
        self.author = args.author
        self.email = args.email
        self.domain = args.domain
        self.protocol = args.protocol
        self.basepath = args.basepath

        self.args = args

    def __repr__(self):
        home = pathlib.Path.home()
        abbrerviated = re.sub(f'^{home}/', '~/', str(self.directory))
        return f'<Site {abbrerviated}>'

    @property
    def uri(self):
        return f'{self.protocol}://{self.domain}{self.basepath}'

    def href(self, path):
        return self.uri + path

    @property
    def entries(self):
        return map(Page,
                   sorted(self.directory.glob('entries/*.html'), reverse=True))

    @property
    def pages(self):
        return map(Page, sorted(self.directory.glob('pages/*.html')))

    @property
    def feed(self):
        return Feed(site=self)

    @property
    def sitemap(self):
        return Sitemap(site=self)

    @functools.cached_property
    def nav(self):
        pages = sorted(filter(lambda p: p.nav_index, self.pages),
                       key=lambda p: p.nav_index)
        return [p.filename for p in pages]

    @functools.cached_property
    def latest(self):
        return next(self.entries, None)

    @functools.cached_property
    def pagination(self):
        pagination = {}
        entries = list(reversed(list(self.entries)))

        for i, entry in enumerate(entries):
            if i > 0:
                previous_entry = entries[i - 1].filename
            else:
                previous_entry = None

            try:
                next_entry = entries[i + 1].filename
            except IndexError:
                next_entry = None

            pagination[entry.filename] = Pagination(next_entry, previous_entry)

        return pagination

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

    def pave(self):
        for page in itertools.chain(self.entries, self.pages,
                                    [self.feed, self.sitemap]):
            target = self.directory / page.target
            if not os.path.exists(target):
                continue
            os.remove(target)
            logger.debug('removed old target %s', target)

    def build(self):
        self.pave()

        for page in self.pages:
            page.build(self)
            logger.info('rendered %s', page)

        self.feed.build()
        logger.info('rendered %s', self.feed)

        self.sitemap.build()
        logger.info('rendered %s', self.sitemap)

        total_entries = sum(1 for _ in self.entries)

        for i, page in enumerate(self.entries):
            page.build(self)
            logger.debug('rendered %s', page)

            # Log an update every 100 entries and at the end of the list
            if (i + 1) % 100 == 0 or (i + 1) == total_entries:
                logger.info('rendered %d out of %d entries', i + 1,
                            total_entries)

    def deploy(self):
        netlify.deploy(site_name=self.domain,
                       token=self.args.netlify_token,
                       webroot=self.directory / 'www')
