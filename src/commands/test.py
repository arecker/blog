"""run the test suite"""

import doctest
import logging
import os
import sys
import unittest

from src.args import get_this_root_directory

logger = logging.getLogger(__name__)


def main(args):
    loader = unittest.TestLoader()
    root_directory = get_this_root_directory()
    modules = loader.discover(start_dir=root_directory / 'src/tests')

    for module in find_modules(root_directory):
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
