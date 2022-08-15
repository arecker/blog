import random

from .. import lib

@lib.register_page(filename='404.html', title='404', description='page not found')
def four_oh_four(renderer=None, entries=[], **kwargs):
    choice = random.choice([e for e in entries if e.banner])
    renderer.block('p', 'I don\'t have that page, so here\'s a random entry instead!')
    renderer.figure(alt='random banner',
                    src=f'./images/banners/{choice.banner}',
                    href=f'./{choice.filename}',
                    caption=choice.description)
    return renderer.text
