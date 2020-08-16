import os


def root():
    actual = os.path.dirname(__file__)

    # TODO: remove after migrate
    return os.path.abspath(os.path.join(actual, '../..'))


def join(*subpaths):
    return os.path.join(root(), *subpaths)


def entries():
    return list(reversed(os.listdir(join('entries'))))
