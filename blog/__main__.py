import datetime

from . import (register_command, run_tests, start_web_server, main, logger,
               root_directory, Page, fetch_git_info)

# TODO: build this dynamically from metadata
nav_pages = ['entries.html', 'projects.html', 'contact.html']


@register_command
def version():
    """print program version"""

    info = fetch_git_info()
    print(info)


@register_command
def test():
    """run program test suite"""

    run_tests()


@register_command
def serve():
    """serve site locally"""

    start_web_server()


def render_page(path, timestamp=None, git_info=None, nav_pages=[]):
    document = Page(path)
    result = document.render(timestamp=timestamp,
                             git_info=git_info,
                             nav_pages=nav_pages)
    target = root_directory.joinpath('www/', document.filename)
    with open(target, 'w+') as f:
        f.write(result)
    logger.debug('rendered %s -> %s', document, target)


@register_command
def build():
    """build the website"""

    start = datetime.datetime.now()

    git_info = fetch_git_info()

    pages = list(sorted(root_directory.glob('pages/*.html')))
    logger.info('building %d pages', len(pages))
    for page in pages:
        render_page(page,
                    timestamp=start,
                    git_info=git_info,
                    nav_pages=nav_pages)

    entries = list(sorted(root_directory.glob('entries/*.md')))
    logger.info('building %d entries', len(entries))
    for page in entries:
        render_page(page,
                    timestamp=start,
                    git_info=git_info,
                    nav_pages=nav_pages)

    elapsed = (datetime.datetime.now() - start).total_seconds()

    logger.info('total build time was %ds', elapsed)


@register_command
def render(source):
    """render a page"""

    document = Page(source)
    logger.info('rendering %s', document)

    timestamp = datetime.datetime.now()
    git_info = fetch_git_info()

    result = document.render(timestamp=timestamp,
                             git_info=git_info,
                             nav_pages=nav_pages)

    print(result)


if __name__ == '__main__':
    main()
