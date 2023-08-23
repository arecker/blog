import collections
import datetime
import logging
import platform
import random

logger = logging.getLogger('blog')


Context = collections.namedtuple('Context', [
    'entries',
    'images',
    'latest',
    'pages',
    'python_version',
    'random',
    'site',
    'this_date',
    'timestamp',
])

Site = collections.namedtuple('Site', [
    'title',
    'description',
    'protocol',
    'domain',
    'author',
    'email',
])


def make_global_context(args=None, entries=[], pages=[], images=[]) -> Context:
    kwargs = {
        'site': Site(
            title=args.site_title,
            description=args.site_description,
            protocol=args.site_protocol,
            domain=args.site_domain,
            author=args.site_author,
            email=args.site_email,
        ),
        'entries': entries,
        'pages': pages,
        'timestamp': datetime.datetime.now(),
        'python_version': platform.python_version(),
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

    return Context(**kwargs)


def on_this_date(entries=[]):
    """
    Find a random entry that occured on the same month and day as the
    first entry in the list.

    Return None if there is No others.
    """

    try:
        latest = entries.pop(0)
    except IndexError:
        return None

    def same_date(e):
        same_month = e.date.month == latest.date.month
        same_day = e.date.day == latest.date.day
        return same_month and same_day

    matching = filter(same_date, entries)
    return random.choice(list(matching))
