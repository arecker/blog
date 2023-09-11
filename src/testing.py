import logging
import unittest

import coverage


logger = logging.getLogger(__name__)


def run_unit_tests() -> int:
    '''
    Runs the whole suite of unit tests.

    Returns the number of executed tests so you have something
    interesting to log.

    >>> logger.info('ran %d test(s)', run_unit_tests())
    '''

    # start unit test coverage recording
    cov = coverage.Coverage()
    cov.start()

    # discover all unit tests
    loader = unittest.TestLoader()
    tests = loader.discover('src', pattern='test_*.py')
    result = unittest.TestResult()
    for test in tests:
        result = test.run(result)

    # stop coverage
    cov.stop()
    cov.save()

    # write html report
    cov.html_report(directory='./www/coverage')

    # return number of tests
    return tests.countTestCases()
