"""generate the site homepage"""

import blog
import logging

from . import utils

logger = logging.getLogger(__name__)


def render_content(latest) -> str:
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

    return html.text


def main(args, entries=[]):
    entries = entries or blog.all_entries(args.directory)
    latest = entries[0]
    logger.info('fetched latest post %s', latest.filename)

    content = render_content(latest=latest).rstrip()

    page = utils.Page(
        filename='index.html',
        title=args.title,
        description=args.subtitle,
        banner=None,
    )
    output = blog.render_page(
        page=page,
        full_url=args.full_url.geturl(),
        content=content,
        author=args.author,
    )

    with open(args.directory / 'www/index.html', 'w') as f:
        f.write(output)
    logger.info('generated index.html')
