import logging
import sys
import unittest

import coverage


logger = logging.getLogger('blog')


def run_unit_tests() -> int:
    '''
    Runs the whole suite of unit tests.

    Returns the number of executed tests so you have something
    interesting to log.

    If any tests fail, the names and stack traces are printed to
    stderr and the whole process is exited.

    >>> logger.info('ran %d test(s)', run_unit_tests())
    '''

    # start unit test coverage recording
    cov = coverage.Coverage()
    cov.start()

    # discover and run all unit tests
    loader = unittest.TestLoader()
    tests = loader.discover('src', pattern='test_*.py')
    result = unittest.TestResult()
    result = tests.run(result)

    # stop coverage
    cov.stop()
    cov.save()

    # report errors
    if result.errors or result.failures:
        logger.error('some unit tests failed!')
        print('', file=sys.stderr)
        for problem in result.errors:
            print(f'=> ERROR: {problem[0]}', file=sys.stderr)
            print(problem[1], file=sys.stderr)
        for problem in result.failures:
            print(f'=> FAILURE: {problem[0]}', file=sys.stderr)
            print(problem[1], file=sys.stderr)
        sys.exit(1)

    # write html report
    cov.html_report(directory='./www/coverage')

    # return number of tests
    return tests.countTestCases()
