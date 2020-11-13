import collections
import glob
import os

from . import shell, paths


IMAGE_EXTENSIONS = (
    '.BMP',
    '.JPEG',
    '.JPG',
    '.PNG',
    '.SVG',
)


Dimensions = collections.namedtuple('Dimensions', 'height width')


def get_dimension(imagepath):
    result = shell.run(f'identify -format "%wx%h" {imagepath}')
    height, width = [int(d.replace('"', '')) for d in result.stdout.split('x')]
    return Dimensions(height, width)


def is_too_big(imagepath):
    dims = get_dimension(imagepath)
    return dims.height > 800 or dims.width > 800


def resize(imagepath):
    shell.run(f'convert {imagepath} -resize 800x800 {imagepath}')


def imagemagick_installed():
    return shell.which('convert')


def is_image(filepath):
    _, ext = os.path.splitext(filepath)
    return ext.upper() in IMAGE_EXTENSIONS


def files():
    return list(filter(is_image, glob.glob(paths.join('images/**/*.*'))))
