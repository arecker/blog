import glob
import os

from .files import join, target
from .logger import info

def files():
    return list(sorted(glob.glob(join('entries/*.*'))))


class Entry(object):
    def __init__(self, source):
        self.source = source

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

    def __repr__(self):
        return f'<Entry {self.filename}>'

    def build(self):
        info(f'building {self} -> {self.relative_target}')


def entries():
    return list(map(Entry, files()))
