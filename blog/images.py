import collections
import logging
import os
import subprocess

logger = logging.getLogger(__name__)


def validate_image_dependencies():
    missing = []

    for command in ['convert', 'identify']:
        result = subprocess.run(['which', command],
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL)
        if result.returncode != 0:
            missing.append(command)

    if missing:
        raise RuntimeError(
            f'Cannot resize images, commands not found in path: {missing}')


Dimensions = collections.namedtuple('Dimensions', ['height', 'width'])


def read_dimensions(path):
    command = ['identify', '-format', '%wx%h', path]
    result = subprocess.run(command, capture_output=True, check=True)
    width, height = result.stdout.decode('UTF-8').split('x')
    return Dimensions(height=int(height), width=int(width))


def is_image(path):
    _, ext = os.path.splitext(path)
    return ext.lower() in (
        '.bmp',
        '.jpeg',
        '.jpg',
        '.png',
    )


def resize_image(path, maxiumum):
    dimensions = f'{maxiumum}x{maxiumum}'
    command = ['convert', path, '-resize', dimensions, '-auto-orient', path]
    subprocess.run(command,
                   check=True,
                   stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)


def check_image(path, maximum=800):
    dimensions = read_dimensions(path)

    if dimensions.height > maximum or dimensions.width > maximum:
        resize_image(path, maximum)
        logger.info('resized %s from %s', path, dimensions)
    else:
        logger.debug('%s is correct size at %s', path, dimensions)
