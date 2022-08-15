import random

from .. import lib


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
