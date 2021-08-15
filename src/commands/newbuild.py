'''
build the website locally
'''

import src as blog


def main(config, context):
    site = blog.site.Site(context.root_directory)
    site.build()
