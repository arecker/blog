"""Render journal entries"""

import blog
import logging

logger = logging.getLogger(__name__)


def main(args, entries=[]):
    entries = entries or blog.all_entries(args.directory / 'entries')

    total = len(entries)
    for i, entry in enumerate(entries):
        with open(args.directory / f'entries/{entry.filename}', 'r') as f:
            content = f.read()

        output = blog.render_entry(entry,
                                   full_url=args.full_url.geturl(),
                                   content=content,
                                   author=args.author)

        with open(args.directory / f'www/{entry.filename}', 'w') as f:
            f.write(output)
        logger.debug('generated %s', entry.filename)
        if (i + 1) % 100 == 0 or (i + 1) == total:
            logger.info('generated %d out of %d entries', i + 1, total)
