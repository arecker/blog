'''
serve webroot locally
'''

import src as blog


def main(config, context):
    blog.start_web_server(context)
