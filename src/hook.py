import logging

from . import lib

logger = logging.getLogger(__name__)


def is_new_staged_image(change) -> bool:
    if change.state != 'added':
        return False

    return lib.is_image(change.path)


def main():
    changes = filter(is_new_staged_image, lib.git_status())

    for change in changes:
        if lib.check_image(change.path):
            lib.git_add(change.path)


if __name__ == '__main__':
    lib.configure_logging()
    main()
