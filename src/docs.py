import logging
import pathlib

import pdoc


logger = logging.getLogger('blog')


def write_api_docs() -> int:
    """
    Generate the website API documentation.

    Returns the total number of generated files so you have something
    interesting to log.

    >>> logger.info('wrote docs - %d file(s)', write_api_docs())
    """

    output_directory = pathlib.Path('./www/api/')

    pdoc.pdoc('src', output_directory=output_directory)

    results = output_directory.glob('**/*')
    results = filter(lambda p: p.is_file(), results)
    results = filter(lambda p: not p.name.startswith('.'), results)
    results = list(results)
    return len(results)
