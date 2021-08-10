import collections
import logging
import os
import subprocess

logger = logging.getLogger(__name__)


def validate_commands():
    missing = []

    for command in ['convert', 'identify']:
        result = subprocess.run(['which', command],
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL)
        if result.returncode != 0:
            missing.append(command)

    return missing


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
        '.gif',
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


def resize_all_images(root_directory=None, maximum=800):
    if missing := validate_commands():
        raise RuntimeError(
            f'Cannot resize images, commands not found in path: {missing}')

    images = list(filter(is_image, root_directory.glob('www/**/*.*')))

    for i, path in enumerate(images):
        check_image(path, maximum=maximum)
        if (i + 1) % 100 == 0 or (i + 1) == len(images):
            logger.info('scanned %d out of %d images', i + 1, len(images))
