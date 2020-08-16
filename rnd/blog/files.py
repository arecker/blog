import os
import shutil

from .logging import logger


def root():
    actual = os.path.dirname(__file__)

    # TODO: remove after migrate
    return os.path.abspath(os.path.join(actual, '../..'))


def join(*subpaths):
    return os.path.join(root(), *subpaths)


def entries():
    files = reversed(os.listdir(join('entries')))
    return [join('entries', f) for f in files]


def href(path):
    relpath = os.path.relpath(path, root())
    return href_root(href_ext('/' + relpath))


def href_ext(path):
    base, ext = os.path.splitext(path)
    return base + {
        '.md': '.html',
    }.get(ext, ext)


def href_root(path):
    special = [
        '/entries/',
        '/pages/'
    ]

    try:
        prefix = next(p for p in special if path.startswith(p))
        return path[len(prefix) - 1:]
    except StopIteration:
        return path


def pave():
    target = join('site')
    logger.debug('paving site path = %s', target)
    shutil.rmtree(target)
    os.mkdir(target)
