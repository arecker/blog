import unittest

from .files import join

test_dir = join('newsrc/test')


def run_tests():
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=test_dir, pattern='test_*.py')
    unittest.TextTestRunner().run(suite)
