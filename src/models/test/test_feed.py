import unittest

from ..feed import Feed


class TestFeedCase(unittest.TestCase):
    def test_repr(self):
        self.assertEqual(repr(Feed()), '<Feed feed.xml>')
