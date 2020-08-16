import functools
import unittest

import coverage

from . import meta, files, entries
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
            'entries': entries.all()
        }

    def build(self, ctx):
        count = len(ctx['entries'])
        logger.info('building %s', plural(count, 'entry', 'entries'))


class Pages(Builder):
    pass


class Coverage(Builder):
    def build(self, ctx):
        logger.info('generating coverage report')
        cov = coverage.Coverage()
        cov.start()
        unittest.main(exit=False, verbosity=0, failfast=True, argv=['discover'])
        cov.stop()
        cov.save()
        print(cov.html_report())
