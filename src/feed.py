import collections


FeedItem = collections.namedtuple('FeedItem', [
    'title',
    'date',
    'date_slug',
    'link',
    'image',
])


def build_feed_items(context) -> list[FeedItem]:
    items = []
    site = context['site']

    for entry in context['entries']:
        link = f'{site.url}/{entry.filename}'
        kwargs = {
            'title': entry.title,
            'date': entry.date,
            'date_slug': entry.date.strftime('%Y-%m-%d'),
            'link': link,
        }
        if entry.banner:
            banner = f'{site.url}/images/banners/{entry.banner}'
            kwargs['image'] = banner
        else:
            kwargs['image'] = None

        items.append(FeedItem(**kwargs))

    for image in sorted(context['images'], key=lambda i: i.path.name):
        # skip banners, since we already have those
        if image.is_banner:
            continue

        link = f'{site.url}/{image.href[2:]}'
        items.append(FeedItem(
            title=image.title,
            date=image.date,
            date_slug=image.date.strftime('%Y-%m-%d'),
            link=link,
            image=link,
        ))

    # sort them all by latest first
    items.sort(key=lambda i: i.date, reverse=True)

    # take first 500
    return items[:500]
