# flake8: noqa
"""run the unittest suite"""

import unittest


def main(*args, **kwargs):
    loader = unittest.TestLoader()
    tests = loader.discover('.')
    testRunner = unittest.runner.TextTestRunner()
    testRunner.run(tests)
