import os
import pathlib
import shutil
import tempfile
import unittest

from .. import utils


class TestWritePage(unittest.TestCase):
    def setUp(self):
        self.tempDir = pathlib.Path(tempfile.mkdtemp())
        os.mkdir(self.tempDir / 'www')

    def tearDown(self):
        shutil.rmtree(self.tempDir)

    def test_valid(self):
        with utils.write_page(self.tempDir, 'test.html') as f:
            f.write('test')

        expected = self.tempDir / 'www/test.html'

        self.assertTrue(expected.exists())
        self.assertTrue(expected.is_file())

    def test_exists(self):
        with utils.write_page(self.tempDir, 'test.html') as f:
            f.write('test')

        with self.assertRaises(FileExistsError):
            with utils.write_page(self.tempDir, 'test.html') as f:
                f.write('test')

    def test_overwrite_ok(self):
        with utils.write_page(self.tempDir, 'test.html') as f:
            f.write('test')

        with utils.write_page(self.tempDir, 'test.html',
                              overwrite_ok=True) as f:
            f.write('test2')

        with open(self.tempDir / 'www/test.html') as f:
            actual = f.read()

        self.assertEqual(actual, 'test2')
