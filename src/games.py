"""generate games pages"""

import collections
import json
import logging
import pathlib

from . import utils

logger = logging.getLogger(__name__)

Game = collections.namedtuple(
    'Game', ['filename', 'title', 'description', 'image', 'category'])


def load_games(directory: pathlib.Path) -> list[Game]:
    games = []

    target = directory / 'data/games.json'
    with open(target, 'r') as f:
        items = json.load(f)

    for item in items:
        games.append(Game(**dict(item.items())))

    return games


def main(args, nav=[]):
    nav = nav or utils.read_nav(args.directory / 'data')
    html = utils.StringWriter(starting_indent=4)

    games = load_games(args.directory)
    logger.info('loaded %d game(s)', len(games))

    categories = sorted(set([game.category for game in games]))

    html.comment('Category Index')
    html.write('<h2>Categories</h2>')
    with html.block('ul'):
        for category in categories:
            with html.block('li'):
                html.write(
                    f'<a href="#{utils.slugify(category)}">{category}</a>')

    for category in categories:
        html.write(f'<h2 id="{utils.slugify(category)}">{category}</h2>',
                   blank=True)

        for game in filter(lambda g: g.category == category, games):
            html.comment(game.title)
            html.write(f'<h3>{game.title}</h3>')
            html.figure(href=f'./{game.filename}',
                        src=f'./images/{game.image}',
                        alt=game.title,
                        caption=game.description)

    page = utils.Page(filename='games.html',
                      title='Games',
                      description='Play Games and Waste Time',
                      banner=None)

    with utils.write_page(args.directory,
                          'games.html',
                          overwrite_ok=args.overwrite) as f:
        f.write(
            utils.render_page(page,
                              full_url=args.full_url,
                              nav_pages=nav,
                              author=args.author,
                              content=html.text.rstrip()))
    logger.info('generated games.html')

    for game in games:
        html = utils.StringWriter()

        with open(args.directory / f'games/{game.filename}') as f:
            content = f.read()
            for line in content.splitlines():
                html.write(line)

        page = utils.Page(filename=game.filename,
                          title=game.title,
                          description=game.description,
                          banner=None)

        with utils.write_page(args.directory, page.filename) as f:
            f.write(html.text.rstrip())
        logger.info('generated %s', game.filename)
