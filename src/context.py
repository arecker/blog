import collections
import datetime
import logging
import random


logger = logging.getLogger('blog')


Context = collections.namedtuple('Context', [
    'entries',
    'images',
    'latest',
    'pages',
    'random',
    'site',
    'this_date',
    'random_napkin',
])


def make_global_context(site, entries=[], pages=[], images=[]) -> Context:
    kwargs = {
        'site': site,
        'entries': entries,
        'pages': pages,
        'images': images,
    }

    try:
        kwargs['latest'] = entries[0]
    except IndexError:
        kwargs['latest'] = None

    this_date = on_this_date(entries)
    if this_date:
        logger.info(
            'on this date - "%s" (%s)',
            this_date.description,
            this_date.filename,
        )
    else:
        logger.info('no "on this date" entry today')
    kwargs['this_date'] = this_date

    # pick a random one with a banner
    kwargs['random'] = random.choice([e for e in entries if e.banner])

    # random napkin
    kwargs['random_napkin'] = random_napkin(images=images)
    if kwargs['random_napkin']:
        logger.info('random napkin art: %s', kwargs['random_napkin'])
    else:
        logger.info('no random napkin art found')

    return Context(**kwargs)


def on_this_date(entries=[]):
    """
    Find a random entry that occured on day as today (but not actually
    today, just the same month and day).

    Return None if there is No others.
    """
    today = datetime.datetime.now()

    def same_date(e):
        same_month = e.date.month == today.month
        same_day = e.date.day == today.day
        different_year = e.date.year != today.year
        return same_month and same_day and different_year

    matching = filter(same_date, entries)

    try:
        return random.choice(list(matching))
    except IndexError:
        return None


def random_napkin(images=[]):
    """Chooses a random napkin image to display"""

    try:
        return random.choice([i for i in images if 'napkin' in (i.slug or '')])
    except IndexError:
        return None
