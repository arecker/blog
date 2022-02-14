"""generate games pages"""

import logging

from . import utils

logger = logging.getLogger(__name__)


def main(args, nav=[]):
    nav = nav or utils.read_nav(args.directory / 'data')
    html = utils.StringWriter(starting_indent=4)

    html.write('<h3>Ghost Busters</h3>')
    html.write(
        '<p>Try to click on as many ghosts as you can before the time runs out, or you will have to suffer - LITERALLY - the spookiest sound ever recorded.  A scratch game.</p>'
    )
    html.write('''
<iframe src="https://scratch.mit.edu/projects/251697814/embed" allowtransparency="true" width="485" height="402" frameborder="0" scrolling="no" allowfullscreen></iframe>
'''.strip())

    html.write('<hr/>')

    html.write('<h3>More to come!</h3>')

    page = utils.Page(filename='games.html',
                      title='Games',
                      description='Play Games and Waste Time',
                      banner=None)
    with open(args.directory / 'www/games.html', 'w') as f:
        f.write(
            utils.render_page(page,
                              full_url=args.full_url,
                              nav_pages=nav,
                              author=args.author,
                              content=html.text.rstrip()))
