'''
resize all images in the webroot
'''

import logging

from blog import images

logger = logging.getLogger(__name__)


def main(args):
    images.validate_image_dependencies()

    all_images = list(
        filter(images.is_image, args.directory.glob('www/**/*.*')))

    for i, path in enumerate(all_images):
        images.check_image(path)
        if (i + 1) % 100 == 0 or (i + 1) == len(all_images):
            logger.info('scanned %d out of %d images', i + 1, len(all_images))
