import glob

from .files import join, target
from .logger import logger as l
from .page import Page


def files():
    return list(reversed(sorted(glob.glob(join('entries/*.*')))))


class Entry(Page):
    pass

def entries():
    return list(map(Entry, files()))
