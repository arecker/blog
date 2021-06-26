#!/usr/bin/env python

from lib import cli, debug, files, lists


@cli.command
def build():
    """
    build the website
    """
    print('building base page context...')
    context = files.Page.context()

    print('building pages...')
    pages = files.pages()
    for page, current, total in lists.count(pages):
        print(f'generating page {current}/{total} - {page}')
        page.generate(context)

    print('building entries...')
    entries = files.entries()
    for entry, current, total in lists.count(entries):
        print(f'generating entry {current}/{total} - {entry}')
        entry.generate(context)


@cli.command
def console():
    """
    open an interactive python shell
    """
    debug.interact()


if __name__ == '__main__':
    cli.main()
