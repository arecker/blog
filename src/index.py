"""generate the site homepage"""

import collections
import datetime
import html as HTML
import json
import logging
import pathlib

from . import git, utils

logger = logging.getLogger(__name__)

NewsItem = collections.namedtuple('NewsItem', ['title', 'description'])


def read_news(directory: pathlib.Path) -> list[NewsItem]:
    target = directory / 'data/news.json'
    with open(target, 'r') as f:
        data = json.load(f)

    news = [NewsItem(**dict(o.items())) for o in data]
    logger.info("loaded %d news item(s) from %s", len(news), target)
    return news


def render_content(latest: utils.Entry,
                   commit: git.Commit,
                   timestamp=None,
                   news=[]) -> str:
    """Render latest post column."""

    html = utils.StringWriter(starting_indent=4)
        
    # Latest Post
    html.comment('Latest Post')
    html.write('<h2>Latest Post</h2>')
    with html.block('a', href=f'./{latest.filename}'):
        html.write(f'<h3 class="title">{latest.title}</h3>',
                   unindent=True)
    html.figure(src=f'./images/banners/{latest.banner}',
                href=f'./{latest.filename}',
                caption=latest.description, blank=True)

    # What's New?
    html.comment('What\'s New?')
    html.write('<h2>What\'s New?</h2>', blank=True)
    for item in news:
        html.write(f'<h3>{item.title}</h3>')
        html.write(f'<p>{item.description}</p>', blank=True)

    # Last Updated
    commit_url = f'https://github.com/arecker/blog/commit/{commit.long_hash}'
    commit_summary = HTML.escape(commit.summary)
    html.comment('Last Updated')
    html.write('<h2>Last Updated</h2>')
    with html.block('p', blank=True):
        with html.block('small'):
            html.write(
                f'[<a href="{commit_url}">{commit.short_hash}</a>]')
            html.br()
            html.write(commit_summary)
        html.br()
        html.small(timestamp)

    return html.text


def new_timestamp() -> str:
    timestamp = datetime.datetime.now()
    timestamp_format = '%A, %B %d %Y %-I:%M %p'
    if zone := timestamp.tzname():
        timestamp_format += f' {zone}'
    else:
        timestamp_format += ' CST'

    return timestamp.strftime(timestamp_format)


def main(args, nav=[]):
    latest = utils.fetch_entries(args.directory / 'entries')[0]
    logger.info('fetched latest post %s', latest.filename)

    commit = git.get_head_commit(args.directory)
    logger.info('fetched head commit \"%s\"', commit.summary)

    timestamp = new_timestamp()
    news = read_news(args.directory)
    content = render_content(latest=latest,
                             commit=commit,
                             timestamp=timestamp,
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

    with utils.write_page(args.directory,
                          'index.html',
                          overwrite_ok=args.overwrite) as f:
        f.write(output)
    logger.info('generated index.html')
