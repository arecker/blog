import sys
import time

from . import (register_command, run_tests, start_web_server, main, logger,
               root_directory, Page)

# TODO: build this dynamically from metadata
nav_pages = ['entries.html', 'projects.html', 'contact.html']


@register_command
def version():
    """print program version"""


@register_command
def test():
    """run program test suite"""

    run_tests()


@register_command
def serve():
    """serve site locally"""

    start_web_server()


@register_command
def build():
    """build the website"""

    start = time.time()

    pages = list(root_directory.glob('pages/*.html'))
    entries = list(root_directory.glob('entries/*.md'))

    logger.info('rendering %d pages, %d entries', len(pages), len(entries))

    for page in pages + entries:
        document = Page(page)
        result = document.render(nav_pages=nav_pages)
        target = root_directory.joinpath('www/', document.filename)
        with open(target, 'w+') as f:
            f.write(result)
        logger.debug('rendered %s -> %s', document, target)

    elapsed = time.strftime("%H:%M:%S", time.gmtime(time.time() - start))

    logger.info('total build time was - %s', elapsed)


@register_command
def render(source):
    """render a page"""

    document = Page(source)
    logger.info('rendering %s', document)

    result = document.render(nav_pages=nav_pages)

    print(result)


if __name__ == '__main__':
    main()
