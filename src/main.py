#!/usr/bin/env python

from lib import cli, debug


@cli.command
def build():
    """
    build the website
    """


@cli.command
def console():
    """
    open an interactive python shell
    """
    debug.interact()


if __name__ == '__main__':
    cli.main()
