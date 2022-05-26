import collections
import logging
import os
import pathlib
import shutil
import subprocess

logger = logging.getLogger(__name__)


def validate_image_dependenices():
    """Find the CLI tools needed for manipulating images."""

    required_commands = ('identify', 'convert')
    missing_commands = [
        c for c in required_commands if not bool(shutil.which(c))
    ]

    if missing_commands:
        raise EnvironmentError(f'cannot find commands: {missing_commands}')


ImageDimensions = collections.namedtuple('ImageDimensions',
                                         ['height', 'width'])


def read_image_dimensions(path) -> ImageDimensions:
    """Read dimensions of an image."""

    command = ['identify', '-format', '%wx%h', str(path)]
    result = subprocess.run(command, capture_output=True, check=True)
    width, height = result.stdout.decode('UTF-8').split('x')
    return ImageDimensions(height=int(height), width=int(width))


def resize_image(path, maximum: int):
    """Resize image to maximum (px), shelling out to convert."""

    path = str(path)
    dims = f'{maximum}x{maximum}'
    cmd = f'convert {path} -resize {dims} -auto-orient {path}'
    subprocess.run(cmd.split(),
                   check=True,
                   stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)


def is_image(path):
    """Return True if path has an image file extension."""

    _, ext = os.path.splitext(str(path))
    return ext.lower() in (
        '.bmp',
        '.jpeg',
        '.jpg',
        '.png',
    )


def is_banner(path):
    """Return True if path is in the banners directory."""

    path = pathlib.Path(path)

    parent = path.parent.name
    grandparent = path.parent.parent.name

    return parent == 'banners' and grandparent == 'images'


def fetch_images(www_directory: str | pathlib.Path) -> list[pathlib.Path]:
    """Retrieve all images in site."""

    root_directory = pathlib.Path(www_directory)
    images = filter(is_image, root_directory.glob('**/*.*'))
    return list(sorted(images))


def check_image(path, maximum=800):
    dimensions = read_image_dimensions(path)

    if dimensions.height > maximum or dimensions.width > maximum:
        resize_image(path, maximum)
        logger.info('resized %s from %s', path, dimensions)
        return True
    else:
        logger.debug('%s is correct size at %s', path, dimensions)
        return False


def scan_images(dir_www: str):
    validate_image_dependenices()

    files = fetch_images(dir_www)
    total = len(files)
    for i, path in enumerate(files):
        check_image(path)
        if (i + 1) % 100 == 0 or (i + 1) == len(files):
            logger.info('checking image sizes %d of %d', i, total)
