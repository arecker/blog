import logging
import pathlib
import unittest


def run_test_suite():
    loader = unittest.TestLoader()
    start_dir = pathlib.Path(__file__).parent.parent.parent
    suite = loader.discover(start_dir)
    runner = unittest.TextTestRunner()

    logger = logging.getLogger()
    current_level = logging.root.level
    logger.setLevel(logging.CRITICAL)
    runner.run(suite)
    logger.setLevel(current_level)
