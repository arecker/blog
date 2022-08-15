import random

from .. import lib


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
