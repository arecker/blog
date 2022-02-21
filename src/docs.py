"""generate code documentation"""

import logging

from . import utils, __doc__ as DOCSTRING

logger = logging.getLogger(__name__)

def main(args, nav=[]):
    nav = nav or utils.read_nav(args.directory / 'data')

    page = utils.Page(filename='blog.html', title='blog', description=DOCSTRING, banner=None)

    content = utils.StringWriter(starting_indent=4)

    name = '<code>blog</code>'

    content.p(f'Let me introduce you to {name}, the ultra-minimal static website builder written in 100% pure python.  Here are some of the selling points.')
    content.ul([
        f'{name} is fast.  There\'s nothing but python running under the hood.',
        f'{name} is simple.  There are no dependencies to wrestle with.',
        f'{name} is extensible.  Drop in your own commands with ease, thanks to the robust API.',
    ])

    content.h2('Getting Started')

    content.p('To get started, just clone the source code.')
    content.pre('$ git clone --depth 1 https://www.github.com/arecker/blog.git ~/src/blog')

    content.p('Set an alias in your shell.')
    content.pre('$ alias blog="cd ~/src/blog && python -m src"')

    content.p('Run the <code>nuke</code> subcommand.')
    content.pre('$ blog nuke')

    content = utils.render_page(page, full_url=args.full_url, content=content.text.rstrip(), nav_pages=nav, author=args.author)

    with utils.write_page(args.directory, page.filename, overwrite_ok=args.overwrite) as f:
        f.write(content)
    logger.info('generated blog.html')
