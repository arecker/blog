import datetime
import unittest
import unittest.mock

from .. import sitemap


class TestSitemap(unittest.TestCase):

    def setUp(self):
        entry = unittest.mock.Mock(date=datetime.datetime(2022, 1, 1),
                                   filename='testy.html')
        self.entries = [entry]
        self.full_url = 'http://bizlocal.biz'

    def test_add_entries(self):
        s = sitemap.Sitemap(self.full_url)
        s.add_entries(self.entries)
        self.assertEqual(len(s.entries), 1)
        actual = s.entries[0]
        self.assertEqual(actual.url, 'http://bizlocal.biz/testy.html')
        self.assertEqual(actual.lastmod, '2022-01-01T00:00:00+00:00')

    def test_locations(self):
        s = sitemap.Sitemap(self.full_url)
        s.add_entries(self.entries)
        self.assertEqual(len(s.locations()), 1)

    def test_len(self):
        s = sitemap.Sitemap(self.full_url)
        s.add_entries(self.entries)
        self.assertEqual(len(s), 1)

    def test_new_sitemap(self):
        s = sitemap.new_sitemap(full_url=self.full_url, entries=self.entries)
        self.assertEqual(len(s.entries), len(self.entries))
        location = s.entries[0]
        self.assertEqual(location.url, self.full_url + '/testy.html')
