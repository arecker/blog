import unittest
import tempfile
import pathlib

from .. import utils


class TestUtils(unittest.TestCase):
    def test_pave_webroot(self):
        with tempfile.TemporaryDirectory() as t:
            webroot = pathlib.Path(t)

            # Delete nothing on an empty directory
            count = utils.pave_webroot(webroot)
            self.assertEqual(count, 0)

            # Delete HTML files
            for i in range(4):
                (webroot / f'{i}.html').touch()
            count = utils.pave_webroot(webroot)
            self.assertEqual(count, 4)

            # Ignore subfolders
            subfolder = (webroot / 'subfolder')
            subfolder.mkdir()
            save_me = subfolder / 'test.html'
            save_me.touch()
            count = utils.pave_webroot(webroot)
            self.assertEqual(count, 0)
            self.assertTrue(save_me.is_file())
