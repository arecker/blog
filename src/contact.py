"""generate contact page"""

import json
import logging

from . import utils

logger = logging.getLogger(__name__)


def load_data(target):
    with open(target, 'r') as f:
        data = json.load(f)
    logger.info('loaded %d key(s) from %s', len(data),
                utils.prettify_path(target))
    return data


def main(args, nav=[]):
    html = utils.StringWriter(starting_indent=4)
    html.figure('./images/me.jpg', alt='me')
    html.p('Here are some different ways you can get in contact with me or find me on the web.')

    data = load_data(args.directory / 'data/contact.json')
    html.dl({
        'Email': f'<a href="mailto:{data["email"]}">{data["email"]}</a>',
        'Twitter': f'<a href="https://www.twitter.com/{data["twitter"]}">{data["twitter"]}</a>',
        'Github': f'<a href="https://www.github.com/{data["github"]}">{data["github"]}</a>',
        'Scratch': f'<a href="https://scratch.mit.edu/users/{data["scratch"]}/">{data["scratch"]}</a>',
    })

    linkedin = f'<a href="https://www.linkedin.com/in/{data["linkedin"]}">LinkedIn</a>'
    gram = f'<a href="https://www.instagram.com/{data["instagram"]}">Instagram</a>'
    fbook = f'<a href="https://www.facebook.com/{data["facebook"]}">Facebook</a>'
    html.p(f'And also {linkedin}, {gram}, and {fbook}.')

    page = utils.Page('contact.html',
                      title='Contact',
                      description='How to Reach Me / Where to Find Me',
                      banner=None)

    nav = nav or utils.read_nav(args.directory / 'data')

    with utils.write_page(args.directory,
                          'contact.html',
                          overwrite_ok=args.overwrite) as f:
        f.write(
            utils.render_page(page,
                              args.full_url,
                              content=html.text.rstrip(),
                              nav_pages=nav,
                              author=args.author))
    logger.info('generated contact.html')
