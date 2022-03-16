"""Generate code documentation"""

import doctest
import html
import logging

from . import utils, __doc__ as DOCSTRING, fetch_package_info, render
from .__main__ import parser

logger = logging.getLogger(__name__)


def render_commands(content: utils.StringWriter):
    content.h2('Commands', _id='commands')

    content.p(
        'All submodules with a <code>main</code> function are callable as subcommands.'
    )

    content.pre(parser.format_help())

    return content


def parse_docstring(docstring: str):
    items = []
    for item in doctest.DocTestParser().parse(docstring):
        if isinstance(item, str):
            item = item.strip()
        items.append(item)

    items = filter(None, items)
    return list(items)


def render_docstring(content: utils.StringWriter,
                     docstring: str) -> utils.StringWriter:

    items = parse_docstring(docstring)
    pre = ''

    while items:

        item = items.pop(0)

        if isinstance(item, str):
            if pre:  # close pre first
                content.pre(pre)
                pre = ''
            content.p(item)
        elif isinstance(item, doctest.Example):
            pre += '>>> ' + html.escape(item.source)
            if item.want:
                pre += html.escape(item.want)
        else:
            raise ValueError(f'don\'t know how to render {type(item)}')

    if pre:
        content.pre(pre)

    return content


def render_api(content: utils.StringWriter):
    content.h2('API', _id='api')

    info = fetch_package_info()

    if info.functions:
        content.h3('Functions')
        content.text += render.render_index(
            headings=info.functions.keys(),
            render_heading=lambda h: f'<code>{h}</code>')

    for k, v in info.functions.items():
        content.h4(f'<code>{k}</code>', _id=render.slugify(k))
        content = render_docstring(content, v.__doc__)

    return content


def main(args, nav=[]):
    nav = nav or utils.read_nav(args.directory / 'data')

    page = utils.Page(filename='blog.html',
                      title='blog',
                      description='API documentation for blog - ' + DOCSTRING,
                      banner=None)

    content = utils.StringWriter(starting_indent=4)

    content.h2('Index')
    content.text += render.render_index(headings=['Commands', 'API'])

    content = render_commands(content)
    content = render_api(content)

    content = utils.render_page(page,
                                full_url=args.full_url,
                                content=content.text.rstrip(),
                                nav_pages=nav,
                                author=args.author)

    with open(args.directory / f'www/{page.filename}', 'w') as f:
        f.write(content)
    logger.info('generated blog.html')
