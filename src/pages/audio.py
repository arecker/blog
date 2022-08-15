import os
import pathlib

from .. import lib


@lib.register_page(filename='audio.html',
                   title='Audio',
                   description='index of website audio files')
def list_audios(renderer=None, args=None, **kwargs):
    audios = list(sorted(pathlib.Path(args.dir_www).glob('audio/**/*.*')))

    with renderer.wrapping_block('table'):
        with renderer.wrapping_block('tr'):
            renderer.block('td', contents='Total Audio Count')
            renderer.block('td', contents=str(len(audios)))
        with renderer.wrapping_block('tr'):
            renderer.block('td', contents='Total Audio Storage')
            total_size = sum([os.path.getsize(i) for i in audios])
            renderer.block('td', contents=lib.convert_size(total_size))

    renderer.divider()

    with renderer.wrapping_block('table'):
        with renderer.wrapping_block('tr'):
            renderer.block('td', contents='Name')
            renderer.block('td', contents='Size')

        for audio in audios:
            with renderer.wrapping_block('tr'):
                with renderer.wrapping_block('td'):
                    name = str(
                        audio.relative_to(
                            pathlib.Path(args.dir_www) / 'audio/'))
                    href = './' + str(
                        audio.relative_to(pathlib.Path(args.dir_www)))
                    renderer.block('a', href=href, contents=name)

                renderer.block('td',
                               contents=lib.convert_size(
                                   os.path.getsize(audio)))

    return renderer.text
