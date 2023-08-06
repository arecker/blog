import collections
import datetime


Context = collections.namedtuple('Context', [
    'site',
    'entries',
    'latest',
    'pages',
    'images',
    'timestamp',
])

Site = collections.namedtuple('Site', [
    'protocol',
    'domain',
    'author',
])


def make_global_context(args=None, entries=[], pages=[], images=[]) -> Context:
    kwargs = {
        'site': Site(
            protocol=args.site_protocol,
            domain=args.site_domain,
            author=args.site_author,
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

    return Context(**kwargs)
