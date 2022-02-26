"""Generate code documentation"""

import doctest
import logging

from . import utils, __doc__ as DOCSTRING, fetch_package_info
from .__main__ import parser

logger = logging.getLogger(__name__)


def render_index(content: utils.StringWriter):
    content.h2('Index')
    content.ul([
        '<a href="#commands">Commands</a>',
        '<a href="#api">API</a>',
    ])
    return content


def render_commands(content: utils.StringWriter):
    content.h2('Commands', _id='commands')

    content.p(
        'All submodules with a <code>main</code> function are callable as subcommands.'
    )

    content.pre(parser.format_help())

    return content


def render_api(content: utils.StringWriter):
    content.h2('API', _id='api')

    info = fetch_package_info()

    docparser = doctest.DocTestParser()

    if info.functions:
        content.h3('Functions')
        for k, v in info.functions.items():
            content.h4(f'<code>{k}</code>')
            for item in docparser.parse(v.__doc__):
                if isinstance(item, str):
                    content.p(item.strip())
                # TODO: parse code examples

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
    content = render_api(content)

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
