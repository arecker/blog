from .. import lib

@lib.register_page(filename='index.html',
                   title='Hey Reader!',
                   description='emails from Alex')
def index(renderer=None, args=None, entries=[], pages=[]):
    latest = entries[0]
    renderer.block('h2', 'Latest Entry')
    renderer.figure(alt='latest entry banner',
                    src=f'./images/banners/{latest.banner}',
                    href=f'./{latest.filename}',
                    caption=latest.description)

    renderer.block('h2', 'Pages')
    pages = [p for p in pages if p.filename not in ('index.html', '404.html')]
    with renderer.wrapping_block('table'):
        for page in pages:
            with renderer.wrapping_block('tr'):
                with renderer.wrapping_block('td'):
                    renderer.block('a',
                                   href=f'./{page.filename}',
                                   contents=page.filename)
                renderer.block('td', contents=page.description)

    renderer.block('h2', 'Feeds')
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
