import collections
import datetime
import pathlib
import re


class NewImage:
    def __init__(self, path):
        self.path = pathlib.Path(path)

    @property
    def filename(self):
        return self.path.name

    @property
    def date(self):
        if match := r_filename.search(self.path.stem):
            return datetime.datetime(
                year=int(match.group('year')),
                month=int(match.group('month')),
                day=int(match.group('day')),
            )
        raise ValueError(f'could not parse date from {self.filename}')

    @property
    def date_slug(self):
        return self.date.strftime('%Y-%m-%d')

    @property
    def slug(self):
        if match := r_filename.search(self.path.stem):
            return match.group('slug')

    @property
    def title(self):
        return self.slug.replace('-', ' ').title()

    @property
    def href(self):
        www_dir = pathlib.Path('./www')
        relpath = self.path.relative_to(www_dir)
        return f'./{relpath}'


Image = collections.namedtuple('Image', [
    'path',
    'banner',
    'entry',
    'src',
    'date',
    'slug',
    'title',
    'alt',
    'napkin',
])

r_filename = re.compile(
    r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})(-(?P<slug>.*))?')


def parse_date(filename: str) -> datetime.datetime:
    """
    Parse the date from a filename with a YYYY-MM-DD- prefix.

    Returns the parsed date and the rest of the image (without the
    file extension).

    >>> parse_date('2023-08-22-test-image.jpg')[0]
    datetime.datetime(2023, 8, 22, 0, 0)
    >>> parse_date('2023-08-22-test-image.jpg')[1]
    'test-image'

    Returns None for the slug if it just has the date in it.
    >>> parse_date('2023-08-22.jpg')[1] is None
    True
    """
    if match := r_filename.match(pathlib.Path(filename).stem):
        return (
            datetime.datetime(
                int(match.group('year')),
                int(match.group('month')),
                int(match.group('day')),
            ),
            match.group('slug'),
        )

    raise ValueError(f'{filename} does not match expected format!')


def load_images(entries=[], images_dir='./www/images/'):
    image_extensions = (
        '.jpg',
        '.jpeg',
        '.png',
    )

    images_dir = pathlib.Path(images_dir)
    banner_dir = images_dir / 'banners'

    images = []

    # organize entries by banner name
    entries = dict([(e.banner, e) for e in entries])

    for p in images_dir.glob('**/*.*'):
        if p.suffix.lower() not in image_extensions:
            continue

        kwargs = {}
        kwargs['path'] = p
        kwargs['src'] = './images/' + str(p.relative_to(images_dir))

        # if its a banner, link the entry
        kwargs['banner'] = banner_dir in p.parents
        kwargs['entry'] = entries.get(p.name)

        # parse the date from the slug
        kwargs['date'], kwargs['slug'] = parse_date(p.name)

        # title for RSS feed
        kwargs['title'] = kwargs['date'].strftime('%Y-%m-%d')
        if slug := kwargs.get('slug'):
            kwargs['title'] += ' - ' + slug.replace('-', ' ').title()

        # use the title as the alt caption
        kwargs['alt'] = kwargs['title']

        # napkin flag
        slug = kwargs['slug']
        kwargs['napkin'] = (slug is not None) and 'napkin' in slug

        images.append(Image(**kwargs))

    return sorted(images, key=lambda i: i.path.name, reverse=True)
