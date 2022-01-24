import datetime
import unittest

from .. import macro
from ..models import Site, Page


class TestExpander(unittest.TestCase):
    def setUp(self):
        self.timestamp = datetime.datetime(year=1990,
                                           month=9,
                                           day=29,
                                           hour=3,
                                           minute=0)
        self.latest = Page(source='2014-11-10.html',
                           is_entry=True,
                           metadata={
                               'title': 'planes, trains, and automobiles',
                               'banner': '2014-11-10.bmp'
                           })

        self.site = Site(entries=[self.latest])
        self.expander = macro.Expander(site=self.site,
                                       timestamp=self.timestamp)
        self.expander.populate()

    def test_expand_timestamp(self):
        actual = self.expander.markup['timestamp']
        expected = 'Saturday, September 29 1990 3:00 AM CST'
        self.assertEqual(actual, expected)

    def test_expand_latest(self):
        actual = self.expander.markup['latest']
        expected = '''
<a href="./2014-11-10.html">
  <h3 class="title">Monday, November 10 2014</h3>
</a>
<figure>
  <a href="./2014-11-10.html">
    <img src="./images/banners/2014-11-10.bmp">
  </a>
  <figcaption>
    <p>planes, trains, and automobiles</p>
  </figcaption>
</figure>'''.strip()
        self.assertEqual(actual, expected)

        del self.latest.metadata['banner']
        self.expander.populate()
        actual = self.expander.markup['latest']
        expected = '''
<a href="./2014-11-10.html">
  <h3 class="title">Thursday, November 10 2014</h3>
</a>
<p>planes, trains, and automobiles</p>
'''.strip()

    def test_expand(self):
        markup = '''
    <div>
      <p>
        <!-- blog:timestamp -->
      </p>
    </div>
'''
        expected = '''
    <div>
      <p>
        Saturday, September 29 1990 3:00 AM CST
      </p>
    </div>
'''
        actual = self.expander.expand(markup)
        self.assertEqual(actual, expected)

        markup = '''
  <div class="row">
    <div class="column">
      <h2>Latest Post</h2>
      <!-- blog:latest -->
    </div>
  </div>
'''
        actual = self.expander.expand(markup)
        expected = '''
  <div class="row">
    <div class="column">
      <h2>Latest Post</h2>
      <a href="./2014-11-10.html">
        <h3 class="title">Monday, November 10 2014</h3>
      </a>
      <figure>
        <a href="./2014-11-10.html">
          <img src="./images/banners/2014-11-10.bmp">
        </a>
        <figcaption>
          <p>planes, trains, and automobiles</p>
        </figcaption>
      </figure>
    </div>
  </div>
'''
        self.assertEqual(actual, expected)
