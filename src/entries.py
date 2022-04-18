"""Render journal entries"""

import blog
import logging

logger = logging.getLogger(__name__)


def main(args, entries=[]):
    entries = entries or blog.all_entries(args.directory)

    total = len(entries)
    for i, entry in enumerate(entries):
        html = blog.Renderer(starting_indent_level=4)

        # copy entry contents
        with open(args.directory / f'entries/{entry.filename}', 'r') as f:
            for line in f.readlines():
                html.write(line.rstrip())

        html.newline()

        html.comment('Pagination')
        with html.wrapping_block('nav'):
            if prev := entry.page_previous:
                html.block('a', contents=f'⟵ {prev}', href=f'./{prev}')

            if entry.page_previous and entry.page_next:
                html.write('&nbsp')

            if nxt := entry.page_next:
                html.block('a', contents=f'{nxt} ⟶', href=f'./{nxt}')

        html.newline()

        output = blog.render_page(entry,
                                   full_url=args.full_url.geturl(),
                                   content=html.text.rstrip(),
                                   author=args.author)
        with open(args.directory / f'www/{entry.filename}', 'w') as f:
            f.write(output)
        logger.debug('generated %s', entry.filename)
        if (i + 1) % 100 == 0 or (i + 1) == total:
            logger.info('generated %d out of %d entries', i + 1, total)
