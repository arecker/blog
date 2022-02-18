import unittest

from .. import utils


class TestPaginateList(unittest.TestCase):
    def test_one(self):
        result = utils.paginate_list(['a', 'b', 'c'])
        self.assertIsNone(result['a'].previous)
        self.assertEqual(result['a'].next, 'b')
        self.assertEqual(result['c'].previous, 'b')
        self.assertIsNone(result['c'].next)
