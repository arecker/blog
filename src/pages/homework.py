import random

from .. import lib


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
