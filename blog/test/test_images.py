import contextlib
import pathlib
import shutil
import subprocess
import unittest
import unittest.mock

from blog import images


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
                'identify -format %wx%h test.jpg'.split(),
                capture_output=True,
                check=True)
            self.assertEqual(dims.width, 80)
            self.assertEqual(dims.height, 70)

    def test_is_image(self):
        self.assertTrue(images.is_image('test.BMP'))
        self.assertTrue(images.is_image('test.JPEG'))
        self.assertTrue(images.is_image('test.JPG'))
        self.assertTrue(images.is_image('test.PNG'))
        self.assertTrue(images.is_image('test.bmp'))
        self.assertTrue(images.is_image('test.jpeg'))
        self.assertTrue(images.is_image('test.jpg'))
        self.assertTrue(images.is_image('test.png'))

        self.assertFalse(images.is_image('Makefile'))
        self.assertFalse(images.is_image('test.GIF'))
        self.assertFalse(images.is_image('test.PY'))
        self.assertFalse(images.is_image('test.SH'))
        self.assertFalse(images.is_image('test.gif'))
        self.assertFalse(images.is_image('test.py'))
        self.assertFalse(images.is_image('test.sh'))

    def test_image_resize(self):
        expected_args = 'convert test.jpg -resize 800x800 -auto-orient test.jpg'
        expected_kwargs = {
            'check': True,
            'stdout': subprocess.DEVNULL,
            'stderr': subprocess.DEVNULL
        }
        with patch_run('') as p:
            images.resize_image('test.jpg', 800)
            p.assert_called_once_with(expected_args.split(), **expected_kwargs)
