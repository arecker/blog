import datetime
import pathlib
import re


r_filename = re.compile(
    r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})(-(?P<slug>.*))?')


class Image:
    """
    A website image.
    """

    def __init__(self, path: str | pathlib.Path, entry=None):
        self._path = pathlib.Path(path)
        self._entry = entry

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
        return self.date_slug == self.path.stem

    @property
    def entry(self):
        """
        The entry where the image is referenced.
        """
        return self._entry


def load_images(entries=[], images_dir='./www/images/') -> list[Image]:
    """
    Loads complete set of images for website as a list of `Image` objects.

    Requires a list of entries so it can associate the entry where it
    is referenced.

    ```python
    images = src.load_images()
    ```
    """

    images = []

    def is_image(p):
        return p.suffix.lower() in (
            '.jpg',
            '.jpeg',
            '.png',
        )

    images_dir = pathlib.Path(images_dir)
    image_files = filter(is_image, images_dir.glob('**/*.*'))

    # build a k/v map of image paths to entries
    ref_map = {}
    for entry in entries:
        for path in entry.extract_links():
            ref_map[str(path)] = entry

    # build the list of images
    for path in image_files:
        images.append(Image(path, ref_map.get(str(path))))

    # finally, sort them by name
    return sorted(images, key=lambda i: i.path.name, reverse=True)
