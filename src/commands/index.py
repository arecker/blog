"""generate the site homepage"""

import collections
import datetime
import json
import logging
import re

from .. import git, utils

logger = logging.getLogger(__name__)

NewsItem = collections.namedtuple('NewsItem', ['title', 'description'])


def read_news(data_dir):
    target = data_dir / 'news.json'
    with open(target, 'r') as f:
        data = json.load(f)

    news = [NewsItem(**dict(o.items())) for o in data]
    logger.info("loaded %d news item(s) from %s", len(news), target)
    return news


def metadata_parse_html(content) -> dict:
    """Parse metadata from magic HTML comments."""
    pattern = re.compile(
        r'^\s?<!--\s?meta:(?P<key>[A-za-z]+)\s?(?P<value>.*)\s?-->$',
        re.MULTILINE)
    values = [(k.strip(), v.strip()) for k, v in pattern.findall(content)]
    return dict(values)


def render_content(latest: utils.Entry,
                   commit: git.Commit,
                   timestamp=None,
                   news=[]) -> str:
    """Render latest post column."""

    html = utils.StringWriter(starting_indent=4)

    with html.block('div', _class='row', blank=True, blank_before=True):
        # Latest Post
        html.comment('Latest Post')
        with html.block('div', _class='column', blank=True):
            html.write('<h2>Latest Post</h2>')
            with html.block('a', href=f'./{latest.filename}'):
                html.write(f'<h3 class="title">{latest.title}</h3>',
                           unindent=True)
            html.figure(src=f'./images/banners/{latest.banner}',
                        href=f'./{latest.filename}',
                        caption=latest.description)

        # Last Updated
        commit_url = f'https://github.com/arecker/blog/commit/{commit.long_hash}'
        commit_summary = commit.summary.replace('&', '&amp;')
        html.comment('Last Updated')
        with html.block('div', _class='column', blank=True):
            html.write('<h2>Last Updated</h2>')
            with html.block('p'):
                with html.block('small', _class='code'):
                    html.write(
                        f'[<a href="{commit_url}">{commit.short_hash}</a>]')
                    html.write('<br/>')
                    html.write(commit_summary)
                html.write('<br/>')
                with html.block('small'):
                    html.write(timestamp)

        # What's New?
        html.write('<!-- What\'s New? -->')
        with html.block('div', _class='column', blank=True):
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


def register(parser):
    return parser


def main(args, nav=[]):
    latest = utils.fetch_entries(args.directory / 'entries')[0]
    logger.info('fetched latest post %s', latest)

    commit = git.get_head_commit()
    logger.info('fetched head commit %s', commit)

    timestamp = new_timestamp()
    news = read_news(args.directory / 'data')
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
        year=args.year,
        author=args.author,
    )
    target = args.directory / 'www/index.html'
    with open(target, 'w') as f:
        f.write(output)
    logger.info('generated index.html')
