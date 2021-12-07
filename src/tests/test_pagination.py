import unittest

from src import pagination


class TestPagination(unittest.TestCase):
    def test_paginate_list(self):

        things = ['a', 'b', 'c']
        pages = pagination.paginate_list(things)

        self.assertIsNone(pages['a'].previous)
        self.assertEqual(pages['a'].next, 'b')
        self.assertEqual(pages['b'].previous, 'a')
        self.assertEqual(pages['b'].next, 'c')
        self.assertEqual(pages['c'].previous, 'b')
        self.assertIsNone(pages['c'].next)
