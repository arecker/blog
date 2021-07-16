from . import register_command, logger, run_tests, start_web_server, main


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


if __name__ == '__main__':
    main()
