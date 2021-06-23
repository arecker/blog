#!/usr/bin/env python

from lib import files, cli

@cli.command
def version(_args):
    """
    print version and exit
    """
    with open(files.join('src/VERSION')) as f:
        print(f.read().strip())


@cli.command
def build(_args):
    """
    build the website
    """


if __name__ == '__main__':
    cli.main()
