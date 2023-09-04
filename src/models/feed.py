import collections

from src.template import render_template


Item = collections.namedtuple('Item', [
    'title',
    'timestamp',
    'path',
    'image',
])


class Feed:
    """
    Website RSS feed.

    An atom feed that you can build from site information and write
    locally as a valid atom RSS feed.
    """

    filename = 'feed.xml'

    def __init__(self, site=None, items: list[Item] = []):  # noqa: E501
        """
        Build a feed object.

        Takes a list of `Item` objects, which is just this named
        tuple:

        ```python
        Item = collections.namedtuple('Item', [
            'title',
            'timestamp',
            'path', # ex. 2020-01-01.html
            'image', # ex. banners/2021-01-01.jpg
        ])
        ```
        """
        self.site = site
        self.items = items

    def render(self):
        content = render_template('feed.xml.j2', context={
            'filename': self.filename,
            'site': self.site,
            'items': self.items,
        })
        # TODO: xscreensaver can't read the feed
        # return xml.prettify(content)
        return content

    def write(self):
        with open(f'./www/{self.filename}', 'w') as f:
            f.write(self.render())

    def __repr__(self):
        return f'<Feed {self.filename}>'


def load_feed(site, entries=[], images=[]) -> Feed:  # noqa: E501
    """
    Load an RSS feed object.

    ```python
    feed = load_feed(site)
    ```
    """
    items = []

    def convert_timestamp(date):
        slug = date.strftime("%Y-%m-%d")
        return f'{slug}T00:00:00+00:00'

    # add all journal entries
    for entry in entries:
        kwargs = {}
        kwargs['title'] = entry.title
        kwargs['path'] = entry.filename

        if entry.banner:
            kwargs['image'] = f'images/banners/{entry.banner}'
        else:
            kwargs['image'] = None

        kwargs['timestamp'] = convert_timestamp(entry.date)
        items.append(Item(**kwargs))

    # add all other images that aren't a banner
    for image in images:
        if image.is_banner:
            continue

        kwargs = {
            'title': image.title,
            'path': f'images/{image.filename}',
            'image': f'images/{image.filename}',
            'timestamp': convert_timestamp(image.date),
        }
        items.append(Item(**kwargs))

    # sort by descending timestamp
    items = sorted(items, key=lambda i: i.timestamp, reverse=True)

    return Feed(site=site, items=items)
