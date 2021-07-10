from newsrc.logger import logger


def paginate_entries(entries=[]):
    logger.info('building pagination for %d entries', len(entries))

    for i, entry in enumerate(entries):
        if i != 0:
            entry.previous_page = entries[i - 1].permalink

        try:
            entry.next_page = entries[i + 1].permalink
        except IndexError:
            pass
