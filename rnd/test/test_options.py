import unittest

from blog import parse_options


class OptionsTestCase(unittest.TestCase):
    def test_parse_options(self):
        actual = parse_options()
        self.assertFalse(actual.verbose, 'should default to not verbose')
        self.assertFalse(actual.silent, 'should default to not silent')

        actual = parse_options(args=['-v', '-s'])
        self.assertTrue(actual.verbose, 'should support verbose switch')
        self.assertTrue(actual.silent, 'should support silent switch')
