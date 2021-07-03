import glob
import os

from .logger import info
from .files import join


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

    def build(self):
        info(f'building {self} -> {self.relative_target}')


def pages():
    return list(map(Page, files()))
