import datetime
import unittest

from src.models import Site, Archive, Page


class TestArchive(unittest.TestCase):
    def setUp(self):
        self.entries = [
            Page(source=f'{year}-01-01.html', is_entry=True)
            for year in (2018, 2019, 2020, 2021)
        ]
        self.entries += [
            Page(source=f'2021-0{month}-01.html', is_entry=True)
            for month in (1, 2, 3, 4, 5)
        ]
        self.site = Site(directory='~/src/blog', entries=self.entries)
        self.archive = Archive(site=self.site)

    def test_repr(self):
        self.assertEqual(repr(self.archive), '<Archive ~/src/blog/entries/>')

    def test_list_years(self):
        self.assertEqual(self.archive.list_years(), [2021, 2020, 2019, 2018])

    def test_list_months(self):
        self.assertEqual(self.archive.list_months(2021), [5, 4, 3, 2, 1])

    def test_list_entries(self):
        entries = self.archive.list_entries(2021, 5)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].date,
                         datetime.datetime(year=2021, month=5, day=1))


class TestPage(unittest.TestCase):
    def test_slug(self):
        page = Page(source='some/directory/page.md')
        self.assertEqual(page.slug, 'page')

    def test_filename(self):
        page = Page(source='some/directory/page.md')
        self.assertEqual(page.filename, 'page.html')