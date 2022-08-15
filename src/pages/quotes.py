import json
import pathlib

from .. import lib

@lib.register_page(filename='quotes.html',
                   title='Quotes',
                   description='collection of my favorite quotes',
                   banner='quotes.jpg')
def quotes_page(renderer=None, args=None, **kwargs):
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
