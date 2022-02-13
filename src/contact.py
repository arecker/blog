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
    with html.block('div', _class='row'):
        with html.block('div', _class='column'):
            html.figure('./images/me.jpg')
        with html.block('div', _class='column'):
            html.write(
                '<p>Here are some different ways you can get in contact with me or find me on the web.</p>'
            )

            data = load_data(args.directory / 'data/contact.json')
            with html.block('dl'):

                # email
                email = data['email']
                html.write('<dt>Email</dt>')
                html.write(f'<dd><a href="mailto:{email}">{email}</a></dd>')

                # twitter
                twitter = data['twitter']
                html.write('<dt>Twitter</dt>')
                html.write(
                    f'<dd><a href="https://www.twitter.com/{twitter}">{twitter}</a></dd>'
                )

                # github
                github = data['github']
                html.write('<dt>Github</dt>')
                html.write(
                    f'<dd><a href="https://www.github.com/{github}">{github}</a></dd>'
                )

                # scratch
                scratch = data['scratch']
                html.write('<dt>Scratch</dt>')
                html.write(
                    f'<dd><a href="https://scratch.mit.edu/users/{scratch}/">{scratch}</a></dd>'
                )

            linkedin, gram, facebook = data['linkedin'], data[
                'instagram'], data['facebook']
            with html.block('p'):
                html.write(f'''
And also <a href="https://www.linkedin.com/in/{linkedin}">LinkedIn</a>, <a href="https://www.instagram.com/{gram}">Instagram</a>, and <a href="https://www.facebook.com/{facebook}">Facebook</a>.
'''.strip())

    page = utils.Page('contact.html',
                      title='Contact',
                      description='How to Reach Me / Where to Find Me',
                      banner=None)
    nav = nav or utils.read_nav(args.directory / 'data')
    with open(args.directory / 'www/contact.html', 'w') as f:
        f.write(
            utils.render_page(page,
                              args.full_url,
                              content=html.text.rstrip(),
                              nav_pages=nav,
                              year=args.year,
                              author=args.author))
    logger.info('generated contact.html')
