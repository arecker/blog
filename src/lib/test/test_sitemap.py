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

    def test_write_sitemap(self):
        with tempfile.TemporaryDirectory() as tmp:
            www = (pathlib.Path(tmp) / 'www')
            www.mkdir()
            sitemap.write_sitemap(www,
                                  full_url=self.full_url,
                                  entries=self.entries)
            actual = www / 'sitemap.xml'
            self.assertTrue(actual.is_file())
