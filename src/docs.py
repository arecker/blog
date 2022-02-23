"""generate code documentation"""

import logging
import pkgutil
import importlib

from . import utils, __doc__ as DOCSTRING, src_dir

logger = logging.getLogger(__name__)


def walk_modules():
    yield importlib.import_module('.', package=src_dir.name)

    for info in sorted(pkgutil.iter_modules([str(src_dir)]),
                       key=lambda m: m.name):
        if info.name == '__main__':
            continue

        yield importlib.import_module(f'.{info.name}', package=src_dir.name)


def render_index(content: utils.StringWriter, modules=[]):
    content.h2('Index')
    items = [f'<code>{m.__name__}</code> -- {m.__doc__}' for m in modules]
    content.ul(items=items)
    return content


def main(args, nav=[]):
    nav = nav or utils.read_nav(args.directory / 'data')

    page = utils.Page(filename='blog.html',
                      title='blog',
                      description='API documentation for blog - ' + DOCSTRING,
                      banner=None)

    content = utils.StringWriter(starting_indent=4)

    modules = [m for m in walk_modules()]
    content = render_index(content, modules=modules)

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
