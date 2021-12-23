import unittest

from src import args


class TestGetDefaultRootDirectory(unittest.TestCase):
    def test_it(self):
        this_file = '/tmp/src/blog/src/args.py'
        actual = str(args.get_this_root_directory(this_file=this_file))
        expected = '/tmp/src/blog'
        self.assertEqual(actual, expected)


class TestDirectory(unittest.TestCase):
    def test_absolute(self):
        actual = str(args.DirectoryType('/tmp'))
        expected = '/tmp'
        self.assertEqual(actual, expected)

    def test_homedir(self):
        actual = str(args.DirectoryType('~/src/blog'))
        self.assertTrue(actual.endswith('src/blog'))
