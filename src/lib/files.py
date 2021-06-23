import os


def root():
    here = os.path.dirname(os.path.realpath(__file__))
    return os.path.abspath(os.path.join(here, '../..'))


def join(*args):
    return os.path.join(root(), *args)
