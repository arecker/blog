#!/usr/bin/env python

from lib import files, args

@args.command
def version():
    """
    print version and exit
    """
    with open(files.join('src/VERSION')) as f:
        print(f.read().strip())


@args.command
def build():
    """
    build the website
    """


if __name__ == '__main__':
    args.main()
