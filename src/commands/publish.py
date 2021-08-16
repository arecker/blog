'''
publish working files as a new entry
'''
import logging

import src as blog

logger = logging.getLogger(__name__)


def main(args):
    blog.validate_image_dependencies()

    new_images = list(
        filter(blog.is_image, blog.git_new_files(args.root_directory)))

    logger.info('checking dimensions for new images: %s', new_images)
    for path in new_images:
        blog.check_image(path)

    blog.git_publish_entry(blog.Site(args))
