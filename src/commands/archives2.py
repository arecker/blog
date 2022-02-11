"""generate journal archives"""

import logging
import urllib.parse

from .. import utils

logger = logging.getLogger(__name__)


def regiser(parser):
    return parser


def main(args):
    html = utils.StringWriter(starting_indent=4)

    # Validate feed link
    html.comment('Validate feed')
    with html.block('p'):
        with html.block('span'):
            link = args.full_url.geturl()
            link = urllib.parse.urljoin(link, 'feed.xml')
            link = urllib.parse.quote_plus(link)
            link = f'https://validator.w3.org/feed/check.cgi?url={link}'
            with html.block('a', href=link):
                src = './assets/valid-atom.png'
                title = 'Validate my Atom 1.0 feed'
                alt = '[Valid Atom 1.0]'
                html.write(f'<img src="{src}" alt="{alt}" title="{title}">')

    print(html.text)
