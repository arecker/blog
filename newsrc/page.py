import functools
import glob
import os

from .banner import BannerMixin
from .config import config
from .files import join, target
from .logger import logger as l
from .metadata import parse_metadata
from .template import render_page


def files():
    return list(sorted(glob.glob(join('pages/*.*'))))


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

    @functools.cached_property
    def context(self):
        twitter = config('twitter')

        return {
            'description': self.description,
            'permalink': self.filename,
            'title': self.title,
            'twitter_handle': twitter['handle'],
        } | self.banner_context


    def render(self):
        return render_page(**self.context)


def pages():
    return list(map(Page, files()))
