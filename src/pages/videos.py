import os
import pathlib
import random

from .. import lib


@lib.register_page(filename='video.html',
                   title='Video',
                   description='index of website videos')
def list_videos(renderer=None, args=None, **kwargs):
    videos = list(sorted(pathlib.Path(args.dir_www).glob('vids/**/*.*')))

    with renderer.wrapping_block('video', controls=""):
        choice = random.choice(videos)
        attrs = {
            'src': './' + str(choice.relative_to(pathlib.Path(args.dir_www))),
            'type': f'video/{choice.suffix[1:]}',
        }
        renderer.block('source', self_closing=True, **attrs)

    with renderer.wrapping_block('table'):
        with renderer.wrapping_block('tr'):
            renderer.block('td', contents='Total Video Count')
            renderer.block('td', contents=str(len(videos)))
        with renderer.wrapping_block('tr'):
            renderer.block('td', contents='Total Video Storage')
            total_size = sum([os.path.getsize(i) for i in videos])
            renderer.block('td', contents=lib.convert_size(total_size))

    renderer.divider()

    with renderer.wrapping_block('table'):
        with renderer.wrapping_block('tr'):
            renderer.block('td', contents='Name')
            renderer.block('td', contents='Size')

        for video in videos:
            with renderer.wrapping_block('tr'):
                with renderer.wrapping_block('td'):
                    name = str(
                        video.relative_to(
                            pathlib.Path(args.dir_www) / 'vids/'))
                    href = './' + str(
                        video.relative_to(pathlib.Path(args.dir_www)))
                    renderer.block('a', href=href, contents=name)

                renderer.block('td',
                               contents=lib.convert_size(
                                   os.path.getsize(video)))

    return renderer.text
