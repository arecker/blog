import collections
import datetime
import random


Context = collections.namedtuple('Context', [
    'site',
    'entries',
    'latest',
    'pages',
    'images',
    'timestamp',
    'random',
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
        'images': images,
    }

    try:
        kwargs['latest'] = entries[0]
    except IndexError:
        kwargs['latest'] = None

    # pick a random one with a banner
    kwargs['random'] = random.choice([e for e in entries if e.banner])

    return Context(**kwargs)
