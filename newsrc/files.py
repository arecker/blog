import os


here = os.path.dirname(os.path.realpath(__file__))
root = os.path.abspath(os.path.join(here, '../'))


def join(*subpaths):
    return os.path.abspath(os.path.join(root, *subpaths))


def target(*subpaths):
    return join('www', *subpaths)


def relative(*subpaths):
    full = join(*subpaths)
    return os.path.relpath(full, start=root)


def whatever_type_by_file(path):
    from .page import Page
    from .entry import Entry

    directory = relative(path).split('/')[0]

    if directory == 'pages':
        return Page(path)
    elif directory == 'entries':
        return Entry(path)