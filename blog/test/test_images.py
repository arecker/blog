import contextlib
import pathlib
import shutil
import subprocess
import unittest
import unittest.mock

from blog import _images as images


@contextlib.contextmanager
def patch_which(installed: list):
    def _which(command):
        return command in installed

    with unittest.mock.patch.object(shutil, 'which', new=_which):
        yield


@contextlib.contextmanager
def patch_run(output):
    result = unittest.mock.Mock(stdout=output.encode('utf-8'))
    with unittest.mock.patch.object(subprocess, 'run',
                                    return_value=result) as patch:
        yield patch


class TestImages(unittest.TestCase):
    def test_validate_image_dependencies(self):
        with patch_which(['identify', 'convert']):
            self.assertIsNone(images.validate_image_dependenices())

        with patch_which(['identify']):
            with self.assertRaises(EnvironmentError) as c:
                images.validate_image_dependenices()
            self.assertEqual(str(c.exception),
                             'cannot find commands: [\'convert\']')

        with patch_which(['convert']):
            with self.assertRaises(EnvironmentError) as c:
                images.validate_image_dependenices()
            self.assertEqual(str(c.exception),
                             'cannot find commands: [\'identify\']')

        with patch_which([]):
            with self.assertRaises(EnvironmentError) as c:
                images.validate_image_dependenices()
            self.assertEqual(
                str(c.exception),
                'cannot find commands: [\'identify\', \'convert\']')

    def test_read_image_dimensions(self):
        with patch_run('80x70') as p:
            dims = images.read_image_dimensions(pathlib.Path('test.jpg'))
            p.assert_called_once_with(
                ['identify', '-format', '%wx%h', 'test.jpg'],
                capture_output=True,
                check=True)
            self.assertEqual(dims.width, 80)
            self.assertEqual(dims.height, 70)
