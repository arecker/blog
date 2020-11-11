import os


SRC = os.path.dirname(os.path.realpath(__file__))
ROOT = os.path.abspath(os.path.join(SRC, '..'))


def join(*paths):
    return os.path.join(ROOT, *paths)
