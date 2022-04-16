"""generate the site homepage"""

import blog
import collections
import datetime
import json
import logging
import pathlib

from . import utils

logger = logging.getLogger(__name__)

NewsItem = collections.namedtuple('NewsItem', ['title', 'description'])


def read_news(directory: pathlib.Path) -> list[NewsItem]:
    target = directory / 'data/news.json'
    with open(target, 'r') as f:
        data = json.load(f)

    news = [NewsItem(**dict(o.items())) for o in data]
    logger.info("loaded %d news item(s) from %s", len(news), target)
    return news


def render_content(latest, timestamp=None, news=[]) -> str:
    """Render latest post column."""

    html = utils.StringWriter(starting_indent=4)

    # Latest Post
    html.comment('Latest Post')
    html.write('<h2>Latest Post</h2>')
    with html.block('a', href=f'./{latest.filename}'):
        html.write(f'<h3 class="title">{latest.title}</h3>', unindent=True)
    html.figure(
        src=f'./images/banners/{latest.banner}',
        href=f'./{latest.filename}',
        caption=latest.description,
        blank=True,
        alt='banner image for latest post',
    )

    # What's New?
    html.comment('What\'s New?')
    html.write('<h2>What\'s New?</h2>', blank=True)
    for item in news:
        html.write(f'<h3>{item.title}</h3>')
        html.write(f'<p>{item.description}</p>', blank=True)

    return html.text


def new_timestamp() -> str:
    timestamp = datetime.datetime.now()
    timestamp_format = '%A, %B %d %Y %-I:%M %p'
    if zone := timestamp.tzname():
        timestamp_format += f' {zone}'
    else:
        timestamp_format += ' CST'

    return timestamp.strftime(timestamp_format)


def main(args, nav=[], entries=[]):
    entries = entries or blog.all_entries(args.directory)
    latest = entries[0]
    logger.info('fetched latest post %s', latest.filename)

    timestamp = new_timestamp()
    news = read_news(args.directory)
    content = render_content(latest=latest, timestamp=timestamp,
                             news=news).rstrip()

    page = utils.Page(
        filename='index.html',
        title=args.title,
        description=args.subtitle,
        banner=None,
    )
    output = utils.render_page(
        page=page,
        full_url=args.full_url,
        content=content,
        nav_pages=nav or utils.read_nav(args.directory / 'data'),
        author=args.author,
    )

    with open(args.directory / 'www/index.html', 'w') as f:
        f.write(output)
    logger.info('generated index.html')
