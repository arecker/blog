import doctest
import os

import blog


def load_tests(loader, tests, ignore):
    python_files = [
        file.name for file in blog.root_directory.glob('blog/*.py')
    ]
    python_identifiers = [os.path.splitext(file)[0] for file in python_files]
    python_modules = [
        f'blog.{identifier}' for identifier in python_identifiers
    ]

    for module in sorted(python_modules):
        blog.logger.debug('adding doctest suite for %s', module)
        tests.addTests(doctest.DocTestSuite(module))

    return tests
