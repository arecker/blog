"""run the test suite"""

import doctest
import logging
import os
import pathlib
import sys
import unittest

logger = logging.getLogger(__name__)
root_dir = pathlib.Path(__file__).parent.parent.parent


def main(args):
    loader = unittest.TestLoader()
    modules = loader.discover(start_dir=str(root_dir / 'blog/test'),
                              pattern='test_*.py')

    for module in find_modules(root_dir):
        modules.addTest(doctest.DocTestSuite(module))
        logger.debug('registered doctests for %s', module)

    runner = unittest.TextTestRunner()
    runner.verbosity = 0
    logger.info('running unit tests')
    if not runner.run(test=modules).wasSuccessful():
        logger.error('test suite failed!')
        sys.exit(1)


def find_modules(root):
    files = root.glob('**/*.py')
    files = [str(f.relative_to(root)) for f in files]
    files = [os.path.splitext(f)[0] for f in files]
    files = [f.replace('/', '.') for f in files]
    return files
