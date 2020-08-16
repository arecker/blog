import unittest

from blog.text import plural


class TextTestCase(unittest.TestCase):
    def test_plural(self):
        actual = plural(1, 'dude')
        expected = '1 dude'
        self.assertEqual(actual, expected, 'should return singular label')

        actual = plural(3, 'dude')
        expected = '3 dudes'
        self.assertEqual(actual, expected, 'should return plural label')

        actual = plural(3, 'box', 'boxen')
        expected = '3 boxen'
        self.assertEqual(actual, expected, 'support custom plurals')
