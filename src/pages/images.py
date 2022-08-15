import pathlib
import random
import os

from .. import lib


@lib.register_page(filename='images.html',
                   title='Images',
                   description='index of website images')
def list_images(renderer=None, args=None, **kwargs):
    images = list(sorted(pathlib.Path(args.dir_www).glob('images/**/*.*')))

    renderer.figure(
        alt='random banner',
        src='./' +
        str(random.choice(images).relative_to(pathlib.Path(args.dir_www))))

    with renderer.wrapping_block('table'):
        with renderer.wrapping_block('tr'):
            renderer.block('td', contents='Total Image Count')
            renderer.block('td', contents=str(len(images)))
        with renderer.wrapping_block('tr'):
            renderer.block('td', contents='Total Image Storage')
            total_size = sum([os.path.getsize(i) for i in images])
            renderer.block('td', contents=lib.convert_size(total_size))

    renderer.divider()

    with renderer.wrapping_block('table'):
        with renderer.wrapping_block('tr'):
            renderer.block('td', contents='Name')
            renderer.block('td', contents='Size')

        for image in images:
            with renderer.wrapping_block('tr'):
                with renderer.wrapping_block('td'):
                    name = str(
                        image.relative_to(
                            pathlib.Path(args.dir_www) / 'images/'))
                    href = './' + str(
                        image.relative_to(pathlib.Path(args.dir_www)))
                    renderer.block('a', href=href, contents=name)

                renderer.block('td',
                               contents=lib.convert_size(
                                   os.path.getsize(image)))

    return renderer.text
