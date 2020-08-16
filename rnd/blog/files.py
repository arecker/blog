import os


def root():
    actual = os.path.dirname(__file__)

    # TODO: remove after migrate
    return os.path.abspath(os.path.join(actual, '../..'))


def join(*subpaths):
    return os.path.join(root(), *subpaths)


def entries():
    return list(reversed(os.listdir(join('entries'))))


def href(path):
    return href_ext('/' + os.path.relpath(path, root()))


def href_ext(path):
    base, ext = os.path.splitext(path)
    return base + {
        '.md': '.html',
    }.get(ext, ext)
