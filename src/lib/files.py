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

    def __repr__(self):
        return f'<Page {self.name}>'

    @property
    def name(self):
        filename = os.path.basename(self.source)
        return os.path.splitext(filename)[0] + '.html'

    def generate(self, context):
        pass


class Entry(Page):
    def __repr__(self):
        return f'<Entry {self.name}>'


def pages():
    paths = sorted(glob.glob(join('pages/*.*')), reverse=True)
    return [Page(p) for p in paths]


def entries():
    paths = sorted(glob.glob(join('entries/*.*')), reverse=True)
    return [Entry(p) for p in paths]
