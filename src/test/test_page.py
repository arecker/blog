import datetime
import unittest

from src import Page


class PageTestCase(unittest.TestCase):
    def test_date(self):
        page = Page('pages/about.html')
        self.assertIsNone(page.date)

        entry = Page('entries/2019-07-02.md')
        expected_date = datetime.datetime(2019, 7, 2)
        self.assertEqual(entry.date, expected_date)

    def test_is_entry(self):
        page = Page('pages/about.html')
        self.assertFalse(page.is_entry())

        entry = Page('entries/2019-07-02.md')
        self.assertTrue(entry.is_entry())
