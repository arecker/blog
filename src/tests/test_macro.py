import datetime
import unittest

from src import macro
from src.models import Site, Page


class TestExpandText(unittest.TestCase):
    def test_expand_text(self):
        timestamp = datetime.datetime(year=1990,
                                      month=9,
                                      day=29,
                                      hour=3,
                                      minute=0)
        site = Site(timestamp=timestamp)
        actual = macro.expand_text('<!-- blog:timestamp -->',
                                   site=site,
                                   suppress_logs=True)
        expected = 'Saturday, September 29 1990 3:00 AM CST'
        self.assertEqual(actual, expected)

    def test_expand_latest(self):
        latest = Page(source='2014-11-10.html',
                      metadata={
                          'title': 'planes, trains, and automobiles',
                          'banner': '2014-11-10.bmp'
                      })
        site = Site(entries=[latest])
        actual = macro.expand_text('<!-- blog:latest -->',
                                   site=site,
                                   suppress_logs=True)
        expected = '''
<a href="/2014-11-10.html">
  <h3 class="title">Thursday, November 10 2014</h3>
</a>
<figure>
  <a href="/2014-11-10.html">
    <img src="/images/banners/2014-11-10.bmp">
  </a>
  <figcaption>
    <p>planes, trains, and automobiles</p>
  </figcaption>
</figure>
'''.strip()
        # self.assertEqual(actual, expected)
