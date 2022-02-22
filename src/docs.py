"""generate code documentation"""

import logging

from . import utils, __doc__ as DOCSTRING

logger = logging.getLogger(__name__)

def main(args, nav=[]):
    nav = nav or utils.read_nav(args.directory / 'data')

    page = utils.Page(filename='blog.html', title='blog', description=DOCSTRING, banner=None)

    content = utils.StringWriter(starting_indent=4)

    content = utils.render_page(page, full_url=args.full_url, content=content.text.rstrip(), nav_pages=nav, author=args.author)

    with utils.write_page(args.directory, page.filename, overwrite_ok=args.overwrite) as f:
        f.write(content)
    logger.info('generated blog.html')
