import glob

from .files import join, target
from .logger import info
from .page import Page


def files():
    return list(sorted(glob.glob(join('entries/*.*'))))


class Entry(Page):
    pass

def entries():
    return list(map(Entry, files()))
