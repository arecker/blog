import os
import glob


def root():
    here = os.path.dirname(os.path.realpath(__file__))
    return os.path.abspath(os.path.join(here, '../..'))


def join(*args):
    return os.path.join(root(), *args)


def target(*args):
    return join('www/', *args)


class Page(object):
    def __init__(self, source):
        self.source = source

    @property
    def name(self):
        filename = os.path.basename(self.source)
        return os.path.splitext(filename)[0] + '.html'

    def __unicode__(self): return self.name

    def __str__(self): return self.__unicode__()


class Entry(Page):
    pass


def pages():
    paths = sorted(glob.glob(join('pages/*.*')))
    return [Page(p) for p in paths]


def entries():
    paths = sorted(glob.glob(join('entries/*.*')))
    return [Entry(p) for p in paths]
