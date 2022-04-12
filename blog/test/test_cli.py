import unittest

from .. import cli


class TestCLI(unittest.TestCase):
    def test_parse_args(self):
        verbose = cli.parse_args(['-v']).verbose
        self.assertTrue(verbose)
