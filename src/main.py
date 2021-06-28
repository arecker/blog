#!/usr/bin/env python

import code
import unittest

import lib as blog


@blog.command
def build():
    """
    build the website
    """
    print('building base page context...')
    context = {}

    print('building pages...')
    pages = blog.pages()
    for page, current, total in blog.count_list(pages):
        print(f'generating page {current}/{total} - {page}')
        page.generate(context)

    print('building entries...')
    entries = blog.entries()
    for entry, current, total in blog.count_list(entries):
        print(f'generating entry {current}/{total} - {entry}')
        entry.generate(context)


@blog.command
def write():
    """
    enter writing mode
    """
    pass


@blog.command
def test():
    """
    run the code unit tests
    """
    testsuite = unittest.TestLoader().discover(blog.join('src/test'))
    unittest.TextTestRunner(verbosity=1).run(testsuite)


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
