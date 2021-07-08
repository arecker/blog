import glob

from .banner import BannerMixin
from .files import join, target
from .logger import logger as l
from .page import Page


def files():
    return list(reversed(sorted(glob.glob(join('entries/*.*')))))


class Entry(Page):
    @property
    def description(self):
        return self.metadata['title']


def entries():
    return list(map(Entry, files()))
