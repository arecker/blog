import unittest
import logging

from ..logging import load_logger


class TestLoadLogger(unittest.TestCase):
    def test_load_logger(self):
        logger = load_logger()
        self.assertEqual(logger.level, logging.INFO)
        logger = load_logger(verbose=True)
        self.assertEqual(logger.level, logging.DEBUG)
