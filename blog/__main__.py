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


def render_page(path):
    document = Page(path)
    result = document.render(nav_pages=nav_pages)
    target = root_directory.joinpath('www/', document.filename)
    with open(target, 'w+') as f:
        f.write(result)
    logger.debug('rendered %s -> %s', document, target)


@register_command
def build():
    """build the website"""

    start = time.time()

    pages = list(sorted(root_directory.glob('pages/*.html')))
    logger.info('building %d pages', len(pages))
    for page in pages:
        render_page(page)

    entries = list(sorted(root_directory.glob('entries/*.md')))
    logger.info('building %d entries', len(entries))
    for page in entries:
        render_page(page)

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
