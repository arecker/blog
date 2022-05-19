import collections
import functools

PAGES = {}

Page = collections.namedtuple('Page', [
    'filename',
    'title',
    'description',
    'banner',
    'render_func',
])


def register_page(filename='', title='', description='', banner=''):
    def wrapper(func):
        functools.wraps(func)
        PAGES[filename] = Page(filename=filename,
                               title=title,
                               description=description,
                               banner=banner,
                               render_func=func)
        return func

    return wrapper
