import datetime
import pathlib
import re


r_filename = re.compile(
    r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})(-(?P<slug>.*))?')


class Image:
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

        # otherwise just return the stem
        return self.path.stem

    @property
    def title(self):
        return self.slug.replace('-', ' ').title()

    @property
    def href(self):
        www_dir = pathlib.Path('./www')
        relpath = self.path.relative_to(www_dir)
        return f'./{relpath}'

    @property
    def is_banner(self):
        banner_dir = pathlib.Path('./www/images/banners/')
        return banner_dir in self.path.parents


def load_images(entries=[], images_dir='./www/images/'):
    image_extensions = (
        '.jpg',
        '.jpeg',
        '.png',
    )

    images_dir = pathlib.Path(images_dir)

    images = []

    for p in images_dir.glob('**/*.*'):
        if p.suffix.lower() not in image_extensions:
            continue
        images.append(Image(p))

    return sorted(images, key=lambda i: i.path.name, reverse=True)
