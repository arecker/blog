import logging
import pathlib
import sys


def configure_logging(
        logger: logging.Logger,
        verbose=False,
        logfile='./www/build.txt',
        truncate_logfile=True
):
    """
    Configure a logger with some sensible defaults.

    Those defaults being:

    1. Log to stderr with a simple formatter
    2. Write last build log to a file in the webroot.

    Extra options:

    - `logfile` path to the logfile
    - `truncate_logfile` whether to truncate the logfile or not
    """
    # formatter
    formatter = logging.Formatter(fmt='blog: %(message)s')

    # level
    if verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO
    logger.setLevel(level)

    # add stderr handler
    stderr_handler = logging.StreamHandler(stream=sys.stderr)
    stderr_handler.setFormatter(formatter)
    stderr_handler.setLevel(level)
    logger.addHandler(stderr_handler)

    # add logfile handler
    file_handler = logging.FileHandler(str(logfile))
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)
    logger.addHandler(file_handler)

    # truncate log file
    with pathlib.Path(logfile).open('w') as f:
        f.write('')

    return logger
