"""publish working files as a new entry"""

import blog
import logging
import os

from . import git, images

logger = logging.getLogger(__name__)


def main(args, entries=[]):
    blog.validate_image_dependenices()

    new_images = blog.all_images(args.directory)

    logger.info('checking dimensions for new images: %s', new_images)
    for path in new_images:
        images.check_image(path)

    git.git_stage_all(args.directory)

    entries = entries or blog.all_entries(args.directory / 'entries')
    latest = entries[0]
    message = f'entry: {latest.title}'
    git.git_write_commit(args.directory, message=message)
    logger.info('added commit: %s', message)

    slug = os.path.splitext(latest.filename)[0]
    tag = f'entry-{slug}'
    git.git_write_tag(args.directory, tag=tag)
    logger.info('created tag %s', tag)

    git.git_push_tag(args.directory, tag=tag)
    logger.info('pushed tag %s', tag)

    git.git_push_master(args.directory)
    logger.info('pushed branch')

    logger.info('successfully published %s (%s)', tag, message)
