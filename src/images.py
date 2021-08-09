import collections
import imghdr
import logging
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


def resize_image(path, maxiumum):
    dimensions = f'{maxiumum}x{maxiumum}'
    command = ['convert', path, '-resize', dimensions, '-auto-orient', path]
    subprocess.run(command,
                   check=True,
                   stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)


def resize_images(root_directory=None, maximum=800):
    if missing := validate_commands():
        raise RuntimeError(
            f'Cannot resize images, commands not found in path: {missing}')

    images = list(root_directory.glob('www/images/**/*.*'))

    for i, path in enumerate(images):
        dimensions = read_dimensions(path)

        if dimensions.height > maximum or dimensions.width > maximum:
            resize_image(path, maximum)
            logger.info('resized %s from %s', path, dimensions)
        else:
            logger.debug('%s is correct size at %s', path, dimensions)

        if (i + 1) % 100 == 0 or (i + 1) == len(images):
            logger.info('scanned %d out of %d images', i + 1, len(images))
