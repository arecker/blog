import unittest

from .. import utils


class TestPrettyPath(unittest.TestCase):
    def test_absolute(self):
        actual = utils.prettify_path('/tmp/thing')
        expected = '/tmp/thing'
        self.assertEqual(actual, expected)

    def test_home(self):
        actual = utils.prettify_path('/home/alex/src/blog', home='/home/alex')
        expected = '~/src/blog'
        self.assertEqual(actual, expected)
