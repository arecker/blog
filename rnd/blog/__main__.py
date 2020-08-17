import logging
import os
import platform
import sys

import blog


def main():
    options = blog.parse_options(args=sys.argv[1:])

    if not options.silent:
        blog.enable_logger(verbose=options.verbose)

    blog.logger.debug('starting blog, python = %s', platform.python_version())
    blog.pave()
    blog.build()


if __name__ == '__main__':
    main()

