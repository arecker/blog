import collections
import datetime
import pathlib
import re


Image = collections.namedtuple('Image', [
    'path',
    'banner',
    'src',
    'date',
    'slug',
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


def load_images(images_dir='./www/images/'):
    image_extensions = (
        '.jpg',
        '.jpeg',
        '.png',
    )

    images_dir = pathlib.Path(images_dir)
    banner_dir = images_dir / 'banners'

    images = []

    for p in images_dir.glob('**/*.*'):
        if p.suffix.lower() not in image_extensions:
            continue

        kwargs = {}
        kwargs['path'] = p
        kwargs['src'] = './images/' + str(p.relative_to(images_dir))
        kwargs['banner'] = banner_dir in p.parents

        # parse the date from the slug
        kwargs['date'], kwargs['slug'] = parse_date(p.name)

        images.append(Image(**kwargs))

    return sorted(images, key=lambda i: i.path.name, reverse=True)
