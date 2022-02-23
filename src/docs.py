"""Generate code documentation"""

import logging

from . import utils, __doc__ as DOCSTRING, src_dir, fetch_commands

logger = logging.getLogger(__name__)


def render_index(content: utils.StringWriter):
    content.h2('Index')
    content.ul([
        f'<a href="#subcommands">Subcommands</a>',
    ])
    return content

def render_commands(content: utils.StringWriter):
    content.h2('Subcommands', _id='subcommands')

    content.p('All submodules with a <code>main</code> function are callable as subcommands.')

    for command in fetch_commands():
        content.h3(f'<code>{command.name}</code>')
        content.p(command.doc)
    
    return content


def main(args, nav=[]):
    nav = nav or utils.read_nav(args.directory / 'data')

    page = utils.Page(filename='blog.html',
                      title='blog',
                      description='API documentation for blog - ' + DOCSTRING,
                      banner=None)

    content = utils.StringWriter(starting_indent=4)
    
    content = render_index(content)
    content = render_commands(content)

    content = utils.render_page(page,
                                full_url=args.full_url,
                                content=content.text.rstrip(),
                                nav_pages=nav,
                                author=args.author)

    with utils.write_page(args.directory,
                          page.filename,
                          overwrite_ok=args.overwrite) as f:
        f.write(content)
    logger.info('generated blog.html')
