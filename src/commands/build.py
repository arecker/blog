'''
build the website locally
'''

import src as blog


def main(args):
    site = blog.Site(args)
    site.build()
