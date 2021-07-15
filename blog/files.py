import os
import pathlib


def make_root_directory_path():
    """Make a copy of the root directory Path object.

    >>> root_directory = make_root_directory_path()
    >>> root_directory.is_dir()
    True
    """

    this_directory = os.path.dirname(os.path.realpath(__file__))
    root_directory_path = os.path.abspath(os.path.join(this_directory, '../'))

    return pathlib.Path(root_directory_path)


root_directory = make_root_directory_path()
