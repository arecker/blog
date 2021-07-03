import os


here = os.path.dirname(os.path.realpath(__file__))
root = os.path.abspath(os.path.join(here, '../'))


def join(*subpaths):
    return os.path.abspath(os.path.join(root, *subpaths))


def target(*subpaths):
    return join('www', *subpaths)
