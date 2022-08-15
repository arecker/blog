import random

from .. import lib


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
