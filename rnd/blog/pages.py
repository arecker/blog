from . import files
from .logging import logger


def entries():
    return [Entry(p) for p in files.entries()]


class Page:
    def __init__(self, src):
        self.src = src

    @property
    def href(self):
        return files.href(self.src)

    def build(self):
        logger.debug('building %s -> %s', self.src, self.href)


class Entry(Page):
    pass
