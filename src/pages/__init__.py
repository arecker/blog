import json
import os
import pathlib
import random
import math

from .. import lib


def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return '{} {}'.format(s, size_name[i])


@lib.register_page(filename='entries.html',
                   title='Entries',
                   description='complete archive of journal entries')
def entries_page(renderer=None, args=None, entries=[], pages=[]):
    entries_with_banners = [e for e in entries if e.banner]
    choice = random.choice(entries_with_banners)
    renderer.figure(alt='random banner',
                    src=f'./images/banners/{choice.banner}',
                    href=f'./{choice.filename}')

    with renderer.wrapping_block('table'):
        for entry in entries:
            with renderer.wrapping_block('tr'):
                with renderer.wrapping_block('td'):
                    renderer.block('a',
                                   href=f'./{entry.filename}',
                                   contents=f'{entry.filename}')
                renderer.block('td', contents=entry.description)

    return renderer.text


@lib.register_page(filename='looking-back.html',
                   title='Looking Back',
                   description='special journal entries that look back in time'
                   )
def looking_back(renderer=None, entries=[], **kwargs):
    entries = list(
        filter(lambda e: e.description.startswith('looking back on'), entries))

    choice = random.choice([e for e in entries if e.banner])
    renderer.figure(alt='random banner',
                    src=f'./images/banners/{choice.banner}',
                    href=f'./{choice.filename}')

    with renderer.wrapping_block('table'):
        for entry in entries:
            with renderer.wrapping_block('tr'):
                with renderer.wrapping_block('td'):
                    renderer.block('a',
                                   href=f'./{entry.filename}',
                                   contents=f'{entry.filename}')
                renderer.block('td', contents=entry.description)

    return renderer.text


@lib.register_page(filename='anti-journal.html',
                   title='Anti-Journal',
                   description='private journal entries re-published')
def anti_journal(renderer=None, entries=[], **kwargs):
    entries = list(
        filter(lambda e: e.description.startswith('anti-journal'), entries))

    choice = random.choice([e for e in entries if e.banner])
    renderer.figure(alt='random banner',
                    src=f'./images/banners/{choice.banner}',
                    href=f'./{choice.filename}')

    with renderer.wrapping_block('table'):
        for entry in entries:
            with renderer.wrapping_block('tr'):
                with renderer.wrapping_block('td'):
                    renderer.block('a',
                                   href=f'./{entry.filename}',
                                   contents=f'{entry.filename}')
                renderer.block('td', contents=entry.description)

    return renderer.text


@lib.register_page(filename='homework.html',
                   title='From the Homework Vault',
                   description='old homework assignments re-published')
def homework_vault(renderer=None, entries=[], **kwargs):
    entries = list(
        filter(lambda e: e.description.startswith('from the homework vault: '),
               entries))

    choice = random.choice([e for e in entries if e.banner])
    renderer.figure(alt='random banner',
                    src=f'./images/banners/{choice.banner}',
                    href=f'./{choice.filename}')

    with renderer.wrapping_block('table'):
        for entry in entries:
            with renderer.wrapping_block('tr'):
                with renderer.wrapping_block('td'):
                    renderer.block('a',
                                   href=f'./{entry.filename}',
                                   contents=f'{entry.filename}')
                renderer.block('td', contents=entry.description)

    return renderer.text

@lib.register_page(filename='images.html', title='Images', description='index of website images')
def list_images(renderer=None, args=None, **kwargs):
    images = list(sorted(pathlib.Path(args.dir_www).glob('images/**/*.*')))

    renderer.figure(alt='random banner',
                    src='./' + str(random.choice(images).relative_to(pathlib.Path(args.dir_www))))

    with renderer.wrapping_block('table'):
        with renderer.wrapping_block('tr'):
            renderer.block('td', contents='Total Image Count')
            renderer.block('td', contents=str(len(images)))
        with renderer.wrapping_block('tr'):
            renderer.block('td', contents='Total Image Storage')
            total_size = sum([os.path.getsize(i) for i in images])
            renderer.block('td', contents=convert_size(total_size))

    renderer.divider()
    
    with renderer.wrapping_block('table'):
        with renderer.wrapping_block('tr'):
            renderer.block('td', contents='Name')
            renderer.block('td', contents='Size')

        for image in images:
            with renderer.wrapping_block('tr'):
                with renderer.wrapping_block('td'):
                    name = str(image.relative_to(pathlib.Path(args.dir_www) / 'images/'))
                    href = './' + str(image.relative_to(pathlib.Path(args.dir_www)))
                    renderer.block('a', href=href, contents=name)

                renderer.block('td', contents=convert_size(os.path.getsize(image)))

    return renderer.text

@lib.register_page(filename='video.html', title='Video', description='index of website videos')
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
            renderer.block('td', contents=convert_size(total_size))

    renderer.divider()
    
    with renderer.wrapping_block('table'):
        with renderer.wrapping_block('tr'):
            renderer.block('td', contents='Name')
            renderer.block('td', contents='Size')

        for video in videos:
            with renderer.wrapping_block('tr'):
                with renderer.wrapping_block('td'):
                    name = str(video.relative_to(pathlib.Path(args.dir_www) / 'vids/'))
                    href = './' + str(video.relative_to(pathlib.Path(args.dir_www)))
                    renderer.block('a', href=href, contents=name)

                renderer.block('td', contents=convert_size(os.path.getsize(video)))

    return renderer.text

@lib.register_page(filename='audio.html', title='Audio', description='index of website audio files')
def list_audios(renderer=None, args=None, **kwargs):
    audios = list(sorted(pathlib.Path(args.dir_www).glob('audio/**/*.*')))

    with renderer.wrapping_block('table'):
        with renderer.wrapping_block('tr'):
            renderer.block('td', contents='Total Audio Count')
            renderer.block('td', contents=str(len(audios)))
        with renderer.wrapping_block('tr'):
            renderer.block('td', contents='Total Audio Storage')
            total_size = sum([os.path.getsize(i) for i in audios])
            renderer.block('td', contents=convert_size(total_size))

    renderer.divider()
    
    with renderer.wrapping_block('table'):
        with renderer.wrapping_block('tr'):
            renderer.block('td', contents='Name')
            renderer.block('td', contents='Size')

        for audio in audios:
            with renderer.wrapping_block('tr'):
                with renderer.wrapping_block('td'):
                    name = str(audio.relative_to(pathlib.Path(args.dir_www) / 'audio/'))
                    href = './' + str(audio.relative_to(pathlib.Path(args.dir_www)))
                    renderer.block('a', href=href, contents=name)

                renderer.block('td', contents=convert_size(os.path.getsize(audio)))

    return renderer.text


from . import four_oh_four
from . import index
from . import napkins
from . import quotes
from . import swears
