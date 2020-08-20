from . import files, markdown
from .logging import logger


def entries():
    return [Entry(p) for p in files.entries()]


class Page:
    def __init__(self, src):
        self.src = src

    @property
    def href(self):
        return files.href(self.src)

    @property
    def is_markdown(self):
        return os.path.splitext(self.src) == '.md'

    def build(self):
        logger.debug('building %s -> %s', self.src, self.href)

    def render(self):
        # if self.is_markdown():
        pass


class Entry(Page):
    pass
