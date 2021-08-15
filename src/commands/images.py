'''
resize all images in the webroot
'''

import src as blog


def main(args):
    blog.resize_all_images(args.root_directory)
