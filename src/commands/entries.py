"""render journal entries"""

import logging

from .. import utils

logger = logging.getLogger(__name__)


def register(parser):
    return parser


def main(args, nav=[], entries=[]):
    nav = nav or utils.read_nav(args.directory / 'data')
    entries = entries or utils.fetch_entries(args.directory / 'entries')

    total = len(entries)
    for i, entry in enumerate(entries):
        html = utils.StringWriter(starting_indent=4)

        # copy entry contents
        with open(args.directory / f'entries/{entry.filename}', 'r') as f:
            for line in f.readlines():
                html.write(line.rstrip())

        html.write('')

        html.comment('Pagination')
        # add pagination
        with html.block('nav', _class='clearfix', blank=True):
            if entry.page_next:
                html.write(
                    f'<a class="float-right" href="./{entry.page_next}">{entry.page_next} ⟶</a>'
                )
            if entry.page_previous:
                html.write(
                    f'<a class="float-left" href="./{entry.page_previous}">⟵ {entry.page_previous}</a>'
                )

        with open(args.directory / f'www/{entry.filename}', 'w') as f:
            output = utils.render_page(entry,
                                       args.full_url,
                                       content=html.text.rstrip(),
                                       nav_pages=nav,
                                       year=args.year,
                                       author=args.author)
            f.write(output)
        logger.debug('generated %s', entry.filename)
        if (i + 1) % 100 == 0 or (i + 1) == total:
            logger.info('generated %d out of %d entries', i + 1, total)
