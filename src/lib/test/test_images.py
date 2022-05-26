import contextlib
import pathlib
import shutil
import subprocess
import tempfile
import unittest
import unittest.mock

from .. import images


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

    def test_resize_image(self):
        with patch_run('') as p:
            images.resize_image('test.jpg', 800)
            cmd = 'convert test.jpg -resize 800x800 -auto-orient test.jpg'
            kwargs = {
                'check': True,
                'stdout': subprocess.DEVNULL,
                'stderr': subprocess.DEVNULL,
            }
            p.assert_called_once_with(cmd.split(), **kwargs)

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
        self.assertFalse(images.is_image('scripts/'))
        self.assertFalse(images.is_image('test.GIF'))
        self.assertFalse(images.is_image('test.gif'))
        self.assertFalse(images.is_image('test.py'))

    def test_is_banner(self):
        self.assertTrue(images.is_banner('./www/images/banner/quotes.png'))

    def test_all_images(self):
        paths = [
            'www/2021-01-01.html',
            'www/assets/style.css',
            'www/images/2021-01-01-apples.jpg',
            'www/images/2021-01-01-fish.jpg',
            'www/images/banners/2021-01-01.jpg',
            'www/index.html',
            'www/vids/2021-01-01-fish-eating.webm',
        ]

        with tempfile.TemporaryDirectory() as d:
            for path in paths:
                path = pathlib.Path(d) / pathlib.Path(path)
                path.parent.mkdir(parents=True, exist_ok=True)
                path.touch(exist_ok=True)

            actual = [str(p.relative_to(d)) for p in images.fetch_images(d)]

            self.assertEqual(actual, [
                'www/images/2021-01-01-apples.jpg',
                'www/images/2021-01-01-fish.jpg',
                'www/images/banners/2021-01-01.jpg',
            ])
