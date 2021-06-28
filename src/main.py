#!/usr/bin/env python

import code

import lib as blog


def count(arglist):
    total = len(arglist)
    for current, thing in enumerate(arglist):
        yield thing, current + 1, total


@blog.command
def build():
    """
    build the website
    """
    print('building base page context...')
    context = {}

    print('building pages...')
    pages = blog.pages()
    for page, current, total in count(pages):
        print(f'generating page {current}/{total} - {page}')
        page.generate(context)

    print('building entries...')
    entries = blog.entries()
    for entry, current, total in count(entries):
        print(f'generating entry {current}/{total} - {entry}')
        entry.generate(context)


@blog.command
def console():
    """
    open an interactive python shell
    """
    try:
        import IPython
        IPython.embed()
    except ImportError:
        code.interact(local=globals())


if __name__ == '__main__':
    blog.main()
