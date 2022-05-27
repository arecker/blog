import logging

from . import git, images

logger = logging.getLogger(__name__)


def is_new_staged_image(change) -> bool:
    if change.state != 'added':
        return False

    return images.is_image(change.path)


def run_pre_commit_hook():
    logger.info('running pre-commit hook')
    changes = list(filter(is_new_staged_image, git.git_status()))

    logger.info('found %d pending changes with images', len(changes))

    for change in changes:
        if images.check_image(change.path):
            git.git_add(change.path)
            logger.info('resized and re-added %s', change.path)
        else:
            logger.info('%s is already correctly sized', change.path)
