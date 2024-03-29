import tempfile
import unittest

from ..page import Page


class TestPage(unittest.TestCase):
    def test_filename(self):
        actual = Page('./pages/index.html').filename
        expected = 'index.html'
        self.assertEqual(actual, expected)

        actual = Page('./pages/index.html.j2').filename
        expected = 'index.html'
        self.assertEqual(actual, expected)

    def test_is_entry(self):
        self.assertFalse(Page('./pages/index.html').is_entry)
        self.assertFalse(Page('./pages/index.html.j2').is_entry)
        self.assertFalse(Page('./pages/index.html.j2').is_entry)
        self.assertTrue(Page('./entries/something.html').is_entry)

    def test_date(self):
        actual = Page('./entries/2023-08-10.html').date
        actual = (actual.year, actual.month, actual.day)
        expected = (2023, 8, 10)
        self.assertEqual(actual, expected)

    def test_metadata(self):
        content = '''
<!-- meta:title A Test Title -->
<!-- meta:description A Test Description -->
        '''

        tmp = tempfile.NamedTemporaryFile()

        with open(tmp.name, 'w') as f:
            f.write(content)

        actual = Page(tmp.name).metadata
        expected = {
            'title': 'A Test Title',
            'description': 'A Test Description',
        }
        self.assertEqual(actual, expected)
