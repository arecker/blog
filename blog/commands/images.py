'''
resize all images in the webroot
'''

import logging
import pathlib

from blog import images

logger = logging.getLogger(__name__)
root_dir = pathlib.Path(__file__).parent.parent.parent


def main(args):
    images.validate_image_dependencies()

    all_images = list(filter(images.is_image, root_dir.glob('www/**/*.*')))

    for i, path in enumerate(all_images):
        images.check_image(path)
        if (i + 1) % 100 == 0 or (i + 1) == len(all_images):
            logger.info('scanned %d out of %d images', i + 1, len(all_images))
