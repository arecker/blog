from . import files


def all():
    return [Entry(p) for p in files.entries()]


class Entry:
    def __init__(self, path):
        self.path = path

