"""generate pets page"""

import logging
import json

from .. import utils

logger = logging.getLogger(__name__)


def register(parser):
    return parser


def load_data(target):
    with open(target, 'r') as f:
        data = json.load(f)
    logger.info('loaded %d pet(s) from %s', len(data),
                utils.prettify_path(target))
    return data


def render_banner(html: utils.StringWriter):
    html.comment('Video Banner')
    with html.block('video',
                    width="800",
                    height="600",
                    autoplay="1",
                    loop="1",
                    blank=True):
        html.write(
            '<source src="./vids/2021-09-07-fish.webm" type="video/webm" />')

    return html


def render_index(html: utils.StringWriter,
                 categories=[]) -> utils.StringWriter:
    html.comment('Index')
    html.write('<h2>Index</h2>')
    with html.block('div', _class='row', blank=True):
        with html.block('ul'):
            for category in categories:
                with html.block('li'):
                    html.write(f'<a href="#{category.lower()}">{category}</a>')
    return html


def render_category(html: utils.StringWriter,
                    category,
                    data=[]) -> utils.StringWriter:
    html.comment(category)
    html.write(f'<h2 id="{category.lower()}">{category}</h2>', blank=True)
    for pet in data:
        name = pet['name']
        logger.debug('rendering pet %s', pet)
        html.comment(name)
        with html.block('div', _class='row', blank=True):
            with html.block('div', _class='column'):
                image = pet['image']
                html.figure(f'./images/{image}')
            with html.block('div', _class='column'):
                html.write(f'<h3>{name}</h3>')
                with html.block('dl'):

                    # species
                    html.write('<dt>Specific name</dt>')
                    with html.block('dd'):
                        html.write(f'<em>{pet["species"]}</em>')

                    # common name
                    html.write('<dt>Common Name</dt>')
                    html.write(f'<dd>{pet["common"]}</dd>')

                    # birthplace
                    try:
                        birthplace = pet['birthplace']
                        html.write('<dt>Birthplace</dt>')
                        html.write(f'<dd>{birthplace}</dd>')
                    except KeyError:
                        pass

                    # gotcha
                    html.write('<dt>Gotcha Date</dt>')
                    html.write(f'<dd>{pet["gotcha"]}</dd>')

                    # aliases
                    try:
                        aliases = pet['aliases']
                        html.write('<dt>Aliases</dt>')
                        html.write(f'<dd>{aliases}</dd>')
                    except KeyError:
                        pass

                    # likes
                    html.write('<dt>Likes</dt>')
                    html.write(f'<dd>{pet["likes"]}</dd>')

                    # dislikes
                    html.write('<dt>Dislikes</dt>')
                    html.write(f'<dd>{pet["dislikes"]}</dd>')

    return html


def main(args, nav=[]):
    nav = nav or utils.read_nav(args.directory / 'data')

    html = utils.StringWriter(starting_indent=4)
    html = render_banner(html)

    html.write('<hr />')

    data = load_data(args.directory / 'data/pets.json')
    categories = sorted(set([pet['category'] for pet in data]))
    html = render_index(html, categories=categories)

    for category in categories:
        pets = [pet for pet in data if pet['category'] == category]
        html = render_category(html, category, data=pets)

    page = utils.Page(filename='pets.html',
                      title='Pets',
                      description='The Recker Family Pet Registy',
                      banner=None)

    with open(args.directory / 'www/pets.html', 'w') as f:
        f.write(
            utils.render_page(page,
                              args.full_url,
                              content=html.text.rstrip(),
                              nav_pages=nav,
                              year=args.year,
                              author=args.author))
    logger.info('generated pets.html')
