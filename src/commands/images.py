'''
resize all images in the webroot
'''

import logging

import src as blog

logger = logging.getLogger(__name__)


def main(args):
    blog.validate_image_dependencies()

    images = list(filter(blog.is_image,
                         args.root_directory.glob('www/**/*.*')))

    for i, path in enumerate(images):
        blog.check_image(path)
        if (i + 1) % 100 == 0 or (i + 1) == len(images):
            logger.info('scanned %d out of %d images', i + 1, len(images))
