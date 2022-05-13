import logging

from . import git, images

logger = logging.getLogger(__name__)


def is_new_staged_image(change: git.GitChange) -> bool:
    if change.state != 'added':
        return False

    return images.is_image(change.path)


def main():
    changes = filter(is_new_staged_image, git.git_status())

    for change in changes:
        if images.check_image(change.path):
            git.git_add(change.path)


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    main()
