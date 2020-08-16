import functools

from . import meta, files, entry
from .text import plural
from .logging import logger


def build():
    context = {}
    builders = [b() for b in meta.descendants(Builder)]
    
    for builder in builders:
        context.update(builder.read())

    for builder in builders:
        builder.build(context)

    for builder in builders:
        builder.validate(context)


class Builder:
    def read(self):
        return {}

    def build(self, ctx):
        pass

    def validate(self, ctx):
        pass


class Entries(Builder):
    def read(self):
        return {
            'entries': self.entries()
        }

    def entries(self):
        return [entry.Entry(p) for p in files.entries()]

    def build(self, ctx):
        count = len(ctx['entries'])
        logger.info('building %s', plural(count, 'entry', 'entries'))


class Pages(Builder):
    pass
