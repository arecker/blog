import collections
import shutil
import subprocess
import os


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

    _, ext = os.path.splitext(path)
    return ext.lower() in (
        '.bmp',
        '.jpeg',
        '.jpg',
        '.png',
    )
