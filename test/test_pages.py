import unittest


from src.page import NewPage


class TestPage(unittest.TestCase):
    def test_filename(self):
        actual = NewPage('./pages/index.html').filename
        expected = 'index.html'
        self.assertEqual(actual, expected)

        actual = NewPage('./pages/index.html.j2').filename
        expected = 'index.html'
        self.assertEqual(actual, expected)

    def test_is_entry(self):
        self.assertFalse(NewPage('./pages/index.html').is_entry)
        self.assertFalse(NewPage('./pages/index.html.j2').is_entry)
        self.assertFalse(NewPage('./pages/index.html.j2').is_entry)
        self.assertTrue(NewPage('./entries/something.html').is_entry)

    def test_date(self):
        actual = NewPage('./entries/2023-08-10.html').date
        actual = (actual.year, actual.month, actual.day)
        expected = (2023, 8, 10)
        self.assertEqual(actual, expected)
