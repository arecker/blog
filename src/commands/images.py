'''
resize all images in the webroot
'''

import src as blog


def main(config, context):
    blog.resize_all_images(context.root_directory)
