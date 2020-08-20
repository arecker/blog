import os

from . import files, markdown, text
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
    def src_extension(self):
        return os.path.splitext(self.src)

    @property
    def target(self):
        return files.join('site', self.href[1:])

    @property
    def raw_content(self):
        with open(self.src, 'r') as f:
            return f.read()

    @property
    def content(self):
        if not hasattr(self, '_content'):
            results = text.extract_frontmatter(self.raw_content)
            self._frontmatter, self._content = results
        return self._content

    @property
    def frontmatter(self):
        if not hasattr(self, '_frontmatter'):
            results = text.extract_frontmatter(self.raw_content)
            self._frontmatter, self._content = results
        return self._frontmatter

    @property
    def is_markdown(self):
        return self.src_extension[1] == '.md'

    def build(self):
        logger.debug('building %s -> %s', self.src, self.href)
        with open(self.target, 'w') as f:
            f.write(self.render())

    def render(self):
        if self.is_markdown:
            try:
                return markdown.convert(self.content)
            except markdown.Problem as e:
                logger.error('problem rendering %s: %s', self.src, e)
                return ''
        return self.content


class Entry(Page):
    pass
