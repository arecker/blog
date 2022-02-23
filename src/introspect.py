"""Functions and objects for introspection and reflection."""

import collections
import importlib
import pathlib
import pkgutil

src_dir: pathlib.Path = pathlib.Path(__file__).absolute().parent
"""source code directory"""
assert src_dir.name == 'src'

Command: collections.namedtuple = collections.namedtuple(
    'Command', ['name', 'doc', 'main_callback', 'register_callback'])
"""submodules with main routines you can run as subcommands"""


def fetch_commands() -> list[Command]:
    """Fetches all subcommands from src as a list of named tuples."""

    commands = []

    package = importlib.import_module('.', package=src_dir.name)

    for info in pkgutil.iter_modules(package.__path__):
        if info.name == '__main__':
            continue

        module = importlib.import_module('.' + info.name, package=src_dir.name)

        try:
            main_callback = module.main
        except AttributeError:
            continue

        try:
            register_callback = module.register
        except AttributeError:  # optional
            register_callback = None

        command = Command(name=info.name,
                          doc=module.__doc__,
                          main_callback=main_callback,
                          register_callback=register_callback)

        commands.append(command)

    return sorted(commands, key=lambda c: c.name)
