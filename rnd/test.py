import os
import unittest

import blog


class FilesTestCase(unittest.TestCase):
    def test_root(self):
        actual = blog.files.root()
        self.assertTrue(os.path.isdir(actual))

    def test_join(self):
        root = blog.files.root()
        actual = blog.files.join('directory/')
        self.assertEqual(actual, os.path.join(root, 'directory/'), 'should join directory')
        actual = blog.files.join('a', 'b', 'c')
        self.assertEqual(actual, os.path.join(root, 'a/b/c'), 'should join multiple directories')

    def test_entries(self):
        entries = blog.files.entries()
        self.assertIsInstance(entries, list, 'entries should be a list')
        self.assertTrue(entries[0] > entries[-1], 'entries should be sorted')


if __name__ == '__main__':
    unittest.main()
