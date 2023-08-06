import collections
import pathlib


Image = collections.namedtuple('Image', [
    'path',
    'banner',
    'src',
])


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

        images.append(Image(**kwargs))

    return sorted(images, key=lambda i: i.path.name, reverse=True)
