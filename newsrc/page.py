import datetime
import functools
import glob
import os

from . import partials
from .banner import BannerMixin
from .config import config
from .files import join, target
from .logger import logger as l
from .metadata import parse_metadata
from .template import render_page


def files():
    return list(sorted(glob.glob(join('pages/*.*'))))


def make_global_context():
    data = {}

    twitter = config('twitter')
    data.update({'twitter_handle': twitter['handle']})

    # partials
    site = config('site')
    now = datetime.datetime.now().astimezone()
    timestamp = now.strftime('%B %-d %Y, %I:%M %p %Z')
    data.update({
        'partial_footer': partials.footer(
            year=now.year,
            author=site['author'],
            timestamp=timestamp,
        )
    })

    return data


class Page(BannerMixin):
    def __init__(self, source):
        self.source = source

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.filename}>'

    @property
    def filename(self):
        base, _ = os.path.splitext(self.source)
        return os.path.basename(base) + '.html'

    @property
    def target(self):
        return target(self.filename)

    @property
    def relative_target(self):
        return f'www/{self.filename}'

    @property
    def permalink(self):
        base, _ = os.path.splitext(self.filename, )
        return f'{base}.html'

    def build(self):
        l.info(f'building {self} -> {self.relative_target}')

    @functools.cached_property
    def metadata(self):
        with open(self.source) as f:
            data, _ = parse_metadata(f.read(), legacy=True)
        return data

    @property
    def title(self):
        return self.metadata['title']

    @property
    def description(self):
        return self.metadata['description']

    @property
    def content(self):
        with open(self.source) as f:
            return f.read()

    @functools.cached_property
    def context(self):
        data={}

        # Page metadata
        data.update({
            'content': self.content,
            'description': self.description,
            'permalink': self.filename,
            'title': self.title,
        } | self.banner_context)

        # Page partials
        data.update({
            'partial_banner': partials.banner(filename=self.banner_filename),
            'partial_header': partials.header(title=self.title, description=self.description),
        })

        return data

    def render(self, global_context={}):
        context = global_context | self.context
        return render_page(**context)


def pages():
    return list(map(Page, files()))
