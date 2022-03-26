import collections
import os
import shutil
import subprocess


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


def is_image(path):
    """Return True if path is an image."""

    _, ext = os.path.splitext(path)

    return ext.lower() in [
        '.bmp',
        '.jpeg',
        '.jpg',
        '.png',
    ]


def resize_image(path, maximum: int):
    """Resize an image to maximum (px) width and height."""

    dimensions = f'{maximum}x{maximum}'
    command = ['convert', path, '-resize', dimensions, '-auto-orient', path]
    subprocess.run(command,
                   check=True,
                   stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)
