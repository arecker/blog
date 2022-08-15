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


@lib.register_page(filename='index.html',
                   title='Dear Journal',
                   description='Daily, public journal by Alex Recker')
def index(renderer=None, args=None, entries=[], pages=[]):
    latest = entries[0]
    renderer.block('h2', 'Latest Entry ☕')
    renderer.figure(alt='latest entry banner',
                    src=f'./images/banners/{latest.banner}',
                    href=f'./{latest.filename}',
                    caption=latest.description)

    renderer.block('h2', 'Pages 🗺')
    pages = [p for p in pages if p.filename not in ('index.html', '404.html')]
    with renderer.wrapping_block('table'):
        for page in pages:
            with renderer.wrapping_block('tr'):
                with renderer.wrapping_block('td'):
                    renderer.block('a',
                                   href=f'./{page.filename}',
                                   contents=page.filename)
                renderer.block('td', contents=page.description)

    renderer.block('h2', 'Feeds 🛰')
    with renderer.wrapping_block('table'):
        with renderer.wrapping_block('tr'):
            with renderer.wrapping_block('td'):
                renderer.block('a', href='./feed.xml', contents='feed.xml')
            renderer.block('td', contents='journal entries')
        with renderer.wrapping_block('tr'):
            with renderer.wrapping_block('td'):
                renderer.block('a',
                               href='./sitemap.xml',
                               contents='sitemap.xml')
            renderer.block('td', contents='complete sitemap')

    return renderer.text


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


@lib.register_page(filename='quotes.html',
                   title='Quotes',
                   description='collection of my favorite quotes',
                   banner='quotes.jpg')
def quotes_Page(renderer=None, args=None, **kwargs):
    target = pathlib.Path(args.dir_data) / 'quotes.json'
    with target.open('r') as f:
        quotes = json.load(f)
    total = len(quotes)

    for i, (author, text) in enumerate(quotes):
        with renderer.wrapping_block('blockquote'):
            renderer.block('p', contents=text)
            renderer.block('p', contents=f'— {author}')
        if i + 1 != total:
            renderer.newline()

    return renderer.text


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

@lib.register_page(filename='404.html', title='404', description='page not found')
def four_oh_four(renderer=None, entries=[], **kwargs):
    choice = random.choice([e for e in entries if e.banner])
    renderer.block('p', 'I don\'t have that page, so here\'s a random entry instead!')
    renderer.figure(alt='random banner',
                    src=f'./images/banners/{choice.banner}',
                    href=f'./{choice.filename}',
                    caption=choice.description)
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


from . import swears
