'''
publish working files as a new entry
'''
import logging

from src import git, images
from src.models import Site

logger = logging.getLogger(__name__)


def main(args):
    images.validate_image_dependencies()

    new_images = list(
        filter(images.is_image, git.git_new_files(args.root_directory)))

    logger.info('checking dimensions for new images: %s', new_images)
    for path in new_images:
        images.check_image(path)

    site = Site(args)

    git.git_stage_all(site.directory)
    message = f'entry: {site.latest.title}'
    git.git_write_commit(site.directory, message=message)
    logger.info('added commit: %s', message)

    tag = f'entry-{site.latest.slug}'
    git.git_write_tag(site.directory, tag=tag)
    logger.info('created tag %s', tag)

    git.git_push_tag(site.directory, tag=tag)
    logger.info('pushed tag %s', tag)

    git.git_push_master(site.directory)
    logger.info('pushed branch')

    logger.info('successfully published %s (%s)', tag, message)
