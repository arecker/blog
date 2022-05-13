import datetime
import pathlib
import tempfile
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

    def test_render_sitemap(self):
        locations = [
            unittest.mock.Mock(url='first', lastmod=None),
            unittest.mock.Mock(url='second', lastmod='this one has a lastmod'),
        ]
        func = unittest.mock.Mock(return_value=locations)
        sm = unittest.mock.Mock(locations=func)

        actual = sitemap.render_sitemap(sm)
        expected = '''
<?xml version="1.0" encoding="utf-8"?>
<urlset xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
  <url>
    <loc>first</loc>
  </url>
  <url>
    <loc>second</loc>
    <lastmod>this one has a lastmod</lastmod>
  </url>
</urlset>
'''.lstrip()
        self.assertEqual(actual, expected)

    def test_write_sitemap(self):
        with tempfile.TemporaryDirectory() as tmp:
            www = (pathlib.Path(tmp) / 'www')
            www.mkdir()
            sitemap.write_sitemap(www,
                                  full_url=self.full_url,
                                  entries=self.entries)
            actual = www / 'sitemap.xml'
            self.assertTrue(actual.is_file())
