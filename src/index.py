"""generate the site homepage"""

import blog
import logging

from . import utils

logger = logging.getLogger(__name__)


def render_content(latest) -> str:
    """Render latest post column."""

    html = blog.Renderer()

    # Latest Post
    html.comment('Latest Post')
    html.block('h2', 'Latest Post')
    with html.wrapping_block('a', href=f'./{latest.filename}'):
        html.block('h3', latest.title)

    html.figure(
        src=f'./images/banners/{latest.banner}',
        href=f'./{latest.filename}',
        caption=latest.description,
        alt='banner image for latest post',
    )

    return html.text


def main(args, entries=[]):
    entries = entries or blog.all_entries(args.directory / 'entries')
    latest = entries[0]
    logger.info('fetched latest post %s', latest.filename)

    content = render_content(latest=latest).rstrip()

    page = utils.Page(
        filename='index.html',
        title=args.title,
        description=args.subtitle,
        banner=None,
        page_next=None,
        page_previous=None,
    )
    output = blog.render_entry(
        page=page,
        full_url=args.full_url.geturl(),
        content=content,
        author=args.author,
    )

    with open(args.directory / 'www/index.html', 'w') as f:
        f.write(output)
    logger.info('generated index.html')
