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

    def test_href(self):
        doc = blog.files.join('doc.txt')
        self.assertEqual(blog.files.href(doc), '/doc.txt', 'should prepend web root to path')

        nested_doc = blog.files.join('images/banners/slavoj.jpeg')
        self.assertEqual(blog.files.href(nested_doc), '/images/banners/slavoj.jpeg', 'should prepend web root to nested path')

        markdown_doc = blog.files.join('test.md')
        self.assertEqual(blog.files.href(markdown_doc), '/test.html', 'should replace markdown extension')

        # markdown_doc = blog.files.join('entries/2020-01-01.md')
        # self.assertEqual(blog.files.href(entry_doc), '/2020-01-01.html', 'should treat entries like root')


if __name__ == '__main__':
    unittest.main()
