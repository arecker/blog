import unittest

from .files import join


def run_tests():
    suite = unittest.TestLoader().discover(
        start_dir=join('newsrc/test'), pattern='test_*.py'
    )
    unittest.TextTestRunner().run(suite)
