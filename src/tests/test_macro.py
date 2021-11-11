import datetime
import unittest

from src import macro
from src.models import Site


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
        self.assertEqual(actual, expected, '<!-- blog:timestamp -->')
