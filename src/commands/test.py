"""run the test suite"""

import doctest
import logging
import os
import unittest

logger = logging.getLogger(__name__)


def main(args):
    loader = unittest.TestLoader()
    modules = loader.discover(start_dir=args.root_directory / 'src/tests')

    for module in find_modules(args.root_directory):
        modules.addTest(doctest.DocTestSuite(module))
        logger.debug('registered doctests for %s', module)

    runner = unittest.TextTestRunner()
    runner.verbosity = 0
    logger.info('running unit tests')
    runner.run(test=modules)


def find_modules(root):
    files = root.glob('**/*.py')
    files = [str(f.relative_to(root)) for f in files]
    files = [os.path.splitext(f)[0] for f in files]
    files = [f.replace('/', '.') for f in files]
    return files
