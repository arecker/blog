import pathlib

from .. import lib


@lib.register_page(filename='napkins.html',
                   title='Napkins',
                   description='gallery of school lunch napkin doodles')
def napkins(renderer=None, args=None, **kwargs):
    images = (pathlib.Path(args.dir_www) / 'images').glob('**/*')
    images = filter(lambda f: f.suffix in ('.png', '.jpg'), images)
    images = filter(lambda i: 'napkin' in i.name, images)
    images = sorted(images, key=lambda i: i.stem, reverse=True)
    images = list(images)
    total = len(images)

    for i, image in enumerate(images):
        src = image.relative_to(args.dir_www)
        renderer.figure(alt=image.stem, src=f'./{src}')
        if i + 1 != total:
            renderer.newline()

    return renderer.text
