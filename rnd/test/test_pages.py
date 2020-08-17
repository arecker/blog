import unittest

from blog import files, pages


class PageTestCase(unittest.TestCase):
    def test_href(self):
        path = files.join('entries/2020-05-05.md')
        actual = pages.Page(path).href
        expected = '/2020-05-05.html'
        self.assertEqual(actual, expected, 'should have expected entry href')
