import glob
import os

from .config import config
from .files import join
from .logger import info


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
        info(f'building {self} -> {self.relative_target}')

    def context(self):
        twitter = config('twitter')
        return {
            'title': self.title,
            'description': self.description,
            'twitter_handle': twitter['handle']
        }


def pages():
    return list(map(Page, files()))
