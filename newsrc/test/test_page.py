import unittest

from newsrc.page import Page


class PageTestCase(unittest.TestCase):
    def test_filename(self):
        actual = Page('some/page/2021-02-21.md').filename
        expected = '2021-02-21.md'
        self.assertEqual(actual, expected)

        actual = Page('pages/test.html').filename
        expected = 'test.html'
        self.assertEqual(actual, expected)
