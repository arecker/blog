#!/usr/bin/env python

from lib import files, cli

@cli.command
def version():
    """
    print version and exit
    """
    with open(files.join('src/VERSION')) as f:
        print(f.read().strip())


@cli.command
def build():
    """
    build the website
    """


if __name__ == '__main__':
    cli.main()
