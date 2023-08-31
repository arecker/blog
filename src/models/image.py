import datetime
import pathlib
import re


r_filename = re.compile(
    r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})(-(?P<slug>.*))?')


class Image:
    """
    A website image.
    """

    def __init__(self, path: str | pathlib.Path):
        self._path = pathlib.Path(path)

    @property
    def path(self) -> pathlib.Path:
        """
        Image as a `pathlib.Path` object.
        """
        return self._path

    @property
    def filename(self):
        """
        Name of the file, ex `test.jpg`
        """
        return self.path.name

    @property
    def date(self) -> datetime.datetime:
        """
        Date, according to the image file's YYY-MM-DD date slug.
        """

        if match := r_filename.search(self.path.stem):
            return datetime.datetime(
                year=int(match.group('year')),
                month=int(match.group('month')),
                day=int(match.group('day')),
            )
        raise ValueError(f'could not parse date from {self.filename}')

    @property
    def date_slug(self):
        """
        Parses the YYYY-MM-DD date slug from the file name.
        """
        return self.date.strftime('%Y-%m-%d')

    @property
    def slug(self):
        """
        The portion of the filename without the extension or the date slug.

        If the full filename is `2023-01-01-fish-soup.png`, the slug
        would be `fish-soup`.
        """
        if match := r_filename.search(self.path.stem):
            return match.group('slug')

        # otherwise just return the stem
        return self.path.stem

    @property
    def title(self):
        """
        Human readable name for the image, based on the date slug.

        For example, `test-image.jpg`, becomes `Test Image`
        """

        return self.slug.replace('-', ' ').title()

    @property
    def href(self):
        """
        The `href` html value that points to the image.

        Can be used in templates like so:

        ```html
        <a href="{{ img.href }}">...</a>
        ```
        """
        www_dir = pathlib.Path('./www')
        relpath = self.path.relative_to(www_dir)
        return f'./{relpath}'

    @property
    def is_banner(self):
        """
        True if the image lives in the banners directory.
        """

        banner_dir = pathlib.Path('./www/images/banners/')
        return banner_dir in self.path.parents


def load_images(entries=[], images_dir='./www/images/') -> list[Image]:
    """
    Loads complete set of images for website as a list of `Image` objects.

    ```python
    images = src.load_images()
    ```
    """

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
