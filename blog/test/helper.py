import unittest

import blog


def run_tests():
    """Run full test suite.

    Runs a complete suite of unit tests and doc tests.  Prints results
    to stdout, just as you would see running it at the commandline.
    """

    loader = unittest.TestLoader()
    test_dir = str(blog.root_directory.joinpath('blog/test'))
    suite = loader.discover(start_dir=test_dir, pattern='test_*.py')
    unittest.TextTestRunner().run(suite)
