import logging
import os
import platform
import sys

import blog


def main():
    blog.enable_logger()
    blog.logger.debug('starting blog, python = %s', platform.python_version())
    blog.pave()
    blog.build()


if __name__ == '__main__':
    main()

