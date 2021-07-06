import functools
import glob
import os

from .config import config
from .files import join, target
from .metadata import parse_metadata
from .files import join
from .logger import logger as l


def files():
    return list(sorted(glob.glob(join('pages/*.*'))))


class Page(object):
    def __init__(self, source):
        self.source = source

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.filename}>'

    @property
    def filename(self):
        return os.path.basename(self.source)

    @property
    def target(self):
        return target(self.filename)

    @property
    def relative_target(self):
        base, _ = os.path.splitext(self.filename, )
        return f'www/{base}.html'

    @property
    def permalink(self):
        base, _ = os.path.splitext(self.filename, )
        return f'{base}.html'

    def build(self):
        l.info(f'building {self} -> {self.relative_target}')

    @functools.cached_property
    def metadata(self):
        with open(self.source) as f:
            data, _ = parse_metadata(f.read())
        return data

    @property
    def title(self):
        return self.metadata['title']

    @functools.cached_property
    def context(self):
        twitter = config('twitter')
        return {
            'title': self.title,
            'description': self.description,
            'twitter_handle': twitter['handle']
        }


def pages():
    return list(map(Page, files()))
