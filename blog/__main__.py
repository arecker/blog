import sys

from . import (register_command, run_tests, start_web_server, main, logger,
               root_directory, Page)


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
def render(source):
    """render a page"""

    document = Page(source)
    logger.info('rendering %s', document)
    print(document.render({}))


if __name__ == '__main__':
    main()