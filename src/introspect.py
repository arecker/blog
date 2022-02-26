"""Functions and objects for introspection and reflection."""

import collections
import importlib
import inspect
import pathlib
import pkgutil

src_dir: pathlib.Path = pathlib.Path(__file__).absolute().parent
"""source code directory"""
assert src_dir.name == 'src'

Command: collections.namedtuple = collections.namedtuple(
    'Command', ['name', 'doc', 'main_callback', 'register_callback'])
"""submodules with main routines you can run as subcommands"""


def fetch_commands() -> list[Command]:
    """Fetches all subcommands from src as a list of named tuples.

    >>> commands = fetch_commands()
    >>> build = next((c for c in commands if c.name == 'build'))
    >>> build.name, build.doc
    ('build', 'Build the website locally')
    """
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


PackageInfo = collections.namedtuple(
    'PackageInfo', ['functions', 'classes', 'variables', 'modules'])
"""Functions, classes, and variables in the top level src package."""
Variable = collections.namedtuple('Variable', ['name', 'docstring'])


def fetch_package_info() -> PackageInfo:
    """Fetch the top level functions, classes, and variables from src.

    Returns a named tuple

    >>> fetch_package_info()._fields
    ('functions', 'classes', 'variables', 'modules')
    """

    package = importlib.import_module('.', package=src_dir.name)

    functions, classes, variables, modules = {}, {}, {}, {}

    for key in dir(package):
        if key.startswith('__'):
            continue

        value = getattr(package, key)

        if inspect.isfunction(value):
            functions[key] = value
        elif inspect.isclass(value):
            classes[key] = value
        elif inspect.ismodule(value):
            modules[key] = value
        else:
            variables[key] = value

    return PackageInfo(functions=functions,
                       classes=classes,
                       variables=variables,
                       modules=modules)
