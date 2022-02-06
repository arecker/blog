"""generate the site homepage"""

import collections
import datetime
import json
import logging
import pathlib
import re

from .. import Document, git

logger = logging.getLogger(__name__)
here = pathlib.Path(__file__).absolute().parent


Post = collections.namedtuple('Post', ['title', 'description', 'banner', 'filename'])
Update = collections.namedtuple('Update', ['title', 'description'])


def fetch_latest() -> Post:
    """Fetch latest post."""

    posts = here.parent.parent.glob('entries/*.html')
    posts = list(sorted(posts, reverse=True))
    latest = posts[0]

    with open(latest, 'r') as f:
        content = f.read()

    metadata = metadata_parse_html(content)

    date = datetime.datetime.strptime(latest.stem, '%Y-%m-%d')
    title = date.strftime('%A, %B %-d %Y')

    return Post(
        title=title,
        description=metadata['title'],
        banner=metadata['banner'],
        filename=latest.name,
    )


def read_news():
    target = here.parent.parent / 'data/news.json'
    with open(target, 'r') as f:
        data = json.load(f)

    news = [Update(**dict(o.items())) for o in data]
    logger.info("loaded %d news item(s) from %s", len(news), target)
    return news


def metadata_parse_html(content) -> dict:
    """Parse metadata from magic HTML comments."""
    pattern = re.compile(
        r'^\s?<!--\s?meta:(?P<key>[A-za-z]+)\s?(?P<value>.*)\s?-->$',
        re.MULTILINE)
    values = [(k.strip(), v.strip()) for k, v in pattern.findall(content)]
    return dict(values)


def render_content(latest: Post, commit: git.Commit, timestamp=None, news=[]) -> str:
    """Render latest post column."""

    news = '\n'.join([f'   <h3>{update.title}</h3>\n   <p>{update.description}</p>' for update in news])

    # TODO: lol
    commit_summary = commit.summary.replace('&', '&amp;')

    return f"""
<div class="row">
  <div class="column">
    <h2>Latest Post</h2>
    <a href="./{latest.filename}">
      <h3 class="title">{latest.title}</h3>
    </a>
    <figure>
      <a href="./{latest.filename}">
        <img src="./images/banners/{latest.banner}" />
      </a>
      <figcaption>
        <p>{latest.description}</p>
      </figcaption>
    </figure>
  </div>
  <div class="column">
    <h2>Last Updated</h2>
    <p>
      <small class="code">
        [<a href="https://github.com/arecker/blog/commit/{commit.long_hash}">{commit.short_hash}</a>]<br/>{commit_summary}
      </small>
      <br/>
      <small>
        {timestamp}
      </small>
    </p>
  </div>
  <div class="column">
    <h2>What's New?</h2>
    {news}
  </div>
</div>""".strip()


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
    latest = fetch_latest()
    logger.info('fetched latest post %s', latest)

    commit = git.get_head_commit()
    logger.info('fetched head commit %s', commit)

    timestamp = new_timestamp()
    news = read_news()
    content = render_content(latest=latest, commit=commit, timestamp=timestamp, news=news)

    document = Document(
        filename='index.html',
        title=args.title,
        description=args.subtitle,
        author=args.author,
        nav_pages=['entries.html', 'pets.html', 'contact.html'],
        content=content,
    )

    target = here.parent.parent / f'www/{document.filename}'
    with open(target, 'w') as f:
        f.write(document.render())
    logger.info('generated %s', target)
