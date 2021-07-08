import unittest

from newsrc import files


class FilesTestCase(unittest.TestCase):
    def test_relative(self):
        relative = 'pages/index.html'
        full = files.join(relative)
        actual = files.relative(full)
        self.assertEqual(actual, relative)
