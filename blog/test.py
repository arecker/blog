import doctest
import importlib
import os
import unittest

from . import root_directory, logger


def all_python_modules():
    """Return a list of all python files"""

    for result in sorted(root_directory.glob('blog/**/*.py')):
        relfile = result.relative_to(root_directory / 'blog/')
        base, _ = os.path.splitext(relfile)
        name = '.' + base.replace('/', '.')
        module = importlib.import_module(name, package='blog')
        logger.debug('imported %s', module)
        yield module


def load_tests(loader, tests, *args):
    for module in all_python_modules():
        test = doctest.DocTestSuite(module)
        tests.addTests(test)
        logger.debug('added %s to test suite', test)

    return tests


def run_tests():
    loader = unittest.TestLoader()
    runner = unittest.TextTestRunner()
    tests = unittest.TestSuite()
    tests = load_tests(loader, tests)
    runner.run(tests)
