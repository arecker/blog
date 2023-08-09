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

    for entry in context.entries:
        kwargs = {
            'title': entry.title,
            'date': entry.date,
            'date_slug': entry.date.strftime('%Y-%m-%d'),
            'link': f'{context.site.protocol}://{context.site.domain}/{entry.filename}',
        }
        if entry.banner:
            kwargs['image'] = f'{context.site.protocol}://{context.site.domain}/images/banner/{entry.banner}',
        else:
            kwargs['image'] = None

        items.append(FeedItem(**kwargs))

    for image in sorted(context.images, key=lambda i: i.path.name):
        link = f'{context.site.protocol}://{context.site.domain}/{image.src[2:]}'
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
