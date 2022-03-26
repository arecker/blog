"""resize images in webroot"""

import logging
import subprocess

import blog

logger = logging.getLogger(__name__)


def resize_image(path, maxiumum):
    dimensions = f'{maxiumum}x{maxiumum}'
    command = ['convert', path, '-resize', dimensions, '-auto-orient', path]
    subprocess.run(command,
                   check=True,
                   stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)


def check_image(path, maximum=800):
    dimensions = blog.read_image_dimensions(path)

    if dimensions.height > maximum or dimensions.width > maximum:
        resize_image(path, maximum)
        logger.info('resized %s from %s', path, dimensions)
    else:
        logger.debug('%s is correct size at %s', path, dimensions)


def main(args):
    blog.validate_image_dependenices()

    all_images = list(filter(blog.is_image, args.directory.glob('www/**/*.*')))

    for i, path in enumerate(all_images):
        try:
            check_image(path)
        except ValueError:
            print(path)
        if (i + 1) % 100 == 0 or (i + 1) == len(all_images):
            logger.info('scanned %d out of %d images', i + 1, len(all_images))
