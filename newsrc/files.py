import os
import contextlib

here = os.path.dirname(os.path.realpath(__file__))
root = os.path.abspath(os.path.join(here, '../'))


@contextlib.contextmanager
def in_root():
    current = os.curdir
    os.chdir(root)
    yield
    os.chdir(current)


def join(*subpaths):
    return os.path.abspath(os.path.join(root, *subpaths))


def target(*subpaths):
    return join('www', *subpaths)


def relative(*subpaths):
    full = join(*subpaths)
    return os.path.relpath(full, start=root)


def whatever_type_by_file(path):
    from .page import Page
    from .entry import entries

    directory = relative(path).split('/')[0]

    if directory == 'pages':
        return Page(path)
    elif directory == 'entries':
        all_entries = entries()
        return next((entry for entry in all_entries if entry.source == path))
