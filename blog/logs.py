import logging
import pathlib
import re


class Formatter(logging.Formatter):
    def format(self, *args, **kwargs):
        result = super().format(*args, **kwargs)
        return prettify_log(result)


def prettify_log(message: str):
    """Prettify a log message."""

    message = re.sub(f'{pathlib.Path.home()}/', '~/', message)
    return message


def configure_logging(verbose=False):
    """Configures root logger."""

    logger = logging.getLogger()

    if verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logger.setLevel(level)

    handler = logging.StreamHandler()
    handler.setLevel(level)

    formatter = Formatter('%(name)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
