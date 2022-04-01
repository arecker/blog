import pathlib
import unittest

from .. import files


class TestFiles(unittest.TestCase):
    def test_is_not_junk_file(self):
        self.assertTrue(files.is_not_junk_file('test.html'))
        self.assertTrue(files.is_not_junk_file(pathlib.Path('test.html')))
        self.assertFalse(files.is_not_junk_file(
            pathlib.Path('.something.tmp')))
        self.assertFalse(files.is_not_junk_file(pathlib.Path('#test.html')))
