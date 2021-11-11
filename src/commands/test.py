"""run the test suite"""

import unittest
import logging

logger = logging.getLogger(__name__)


def main(args):
    loader = unittest.TestLoader()
    modules = loader.discover(start_dir=args.root_directory / 'src/tests')
    runner = unittest.TextTestRunner()
    runner.verbosity = 0

    logger.info('running %d test case(s)', modules.countTestCases())
    runner.run(test=modules)
