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


def render_content(latest: utils.Entry, commit: git.Commit, timestamp=None, news=[]) -> str:
    """Render latest post column."""

    html = utils.StringWriter(starting_indent=4)

    # row: begin
    html.write('<div class="row">', indent=True, blank=True)

    # Latest Post
    html.write('<!-- Latest Post -->')
    html.write('<div class="column">', indent=True)
    html.write('<h2>Latest Post</h2>')

    with html.wrapper('a', href=f'./{latest.filename}'):
        html.write(f'<h3 class="title">{latest.title}</h3>', unindent=True)
    with html.wrapper('figure'):
        with html.wrapper('a', href=f'./{latest.filename}'):
            html.write(f'<img src="./images/banners/{latest.banner}" />')
        with html.wrapper('figcaption'):
            html.write(f'<p>{latest.description}</p>', unindent=True)

    html.unindent()
    html.write('</div>', blank=True)

    html.write('<!-- Last Updated -->')
    html.write('<div class="column">', indent=True)
    html.write('<h2>Last Updated</h2>')
    html.write('<p>', indent=True)
    html.write('<small class="code">', indent=True)
    commit_url = f'https://github.com/arecker/blog/commit/{commit.long_hash}'
    commit_summary = commit.summary.replace('&', '&amp;')
    html.write(f'[<a href="{commit_url}">{commit.short_hash}</a>]<br/>{commit_summary}', unindent=True)
    html.write('</small>')
    html.write('<br/>')
    html.write('<small>', indent=True)
    html.write(timestamp, unindent=True)
    html.write('</small>', unindent=True)
    html.write('</p>', unindent=True)
    html.write('</div>', blank=True)

    html.write('<!-- What\'s New? -->')
    html.write('<div class="column">', indent=True)
    html.write('<h2>What\'s New?</h2>')
    for item in news:
        html.write(f'<h3>{item.title}</h3>')
        html.write(f'<p>{item.description}</p>')
    html.unindent()
    html.write('</div>', unindent=True, blank=True)

    html.write('</div>')
    # row: end

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


def main(args):
    latest = utils.fetch_entries(args.directory / 'entries')[0]
    logger.info('fetched latest post %s', latest)

    commit = git.get_head_commit()
    logger.info('fetched head commit %s', commit)

    timestamp = new_timestamp()
    news = read_news(args.directory / 'data')
    content = render_content(
        latest=latest,
        commit=commit,
        timestamp=timestamp,
        news=news
    ).rstrip()

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
        nav_pages=['entries.html', 'pets.html', 'contact.html'],
        year=args.year,
        author=args.author,
    )
    target = args.directory / 'www/index.html'
    with open(target, 'w') as f:
        f.write(output)
    logger.info('generated index.html')
