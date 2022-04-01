import pathlib


def is_not_junk_file(path: str | pathlib.Path):
    """Returns true if the file is not a hidden file or an auto-save file.

    >>> is_not_junk_file(pathlib.Path('test.html'))
    True

    >>> is_not_junk_file(pathlib.Path('#.test.html'))
    False

    >>> is_not_junk_file(pathlib.Path('.test.html'))
    False
    """
    path = pathlib.Path(path)
    first_char = path.name[0]
    return first_char not in ('#', '.')
