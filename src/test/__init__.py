# flake8: noqa
"""run the unittest suite"""

import doctest
import importlib
import logging
import pathlib
import pkgutil
import sys
import unittest

logger = logging.getLogger(__name__)


def discover_tests():
    src = pathlib.Path(__file__).absolute().parent.parent
    assert src.name == 'src'
    tests = []
    for suite in unittest.TestLoader().discover(src):
        for test in suite:
            tests.append(test)
    return tests


def main(*args, **kwargs):
    failed = False
    tests = discover_tests()
    for test in tests:
        result = unittest.TestResult()
        test.run(result)
        if result.wasSuccessful():
            logger.debug('%s was successful', test)
        else:
            failed = True
            for test_case, test_trace in result.errors + result.failures:
                logger.error('%s failed\n%s', test_case, test_trace)

    if failed:
        logger.error('the test suite was not successful!')
        sys.exit(1)

    logger.info('%d test(s) succeeded', len(tests))
            

def load_tests(loader: unittest.TestLoader, tests: unittest.TestSuite, pattern: str):

    src = importlib.import_module('.', package='src')

    for importer, name, ispkg in pkgutil.walk_packages(src.__path__, src.__name__ + '.'):
        tests.addTests(doctest.DocTestSuite(name))

    return tests
