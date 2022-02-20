"""generate stats page"""

import logging
import pathlib

from . import utils

logger = logging.getLogger(__name__)


def count_lines_of_code(src_dir: pathlib.Path) -> int:
    python_files = list(src_dir.glob('**/*.py'))

    total = 0
    for p in python_files:
        with open(p, 'r') as f:
            total += len(f.readlines())

    return total


def find_max_and_min_length(entries_dir: pathlib.Path, entries):
    def count_length(e):
        target = entries_dir / e.filename
        with open(target, 'r') as f:
            return len(f.read())

    by_length = sorted(entries, key=count_length, reverse=True)
    return by_length[0], by_length[-1]


def main(args, nav=[], entries=[]):
    nav = nav or utils.read_nav(args.directory / 'data')
    entries = entries or utils.fetch_entries(args.directory / 'entries')

    webroot = args.directory / 'www'

    data = {}
    data['Number of images'] = len(list(webroot.glob('images/**/*.*')))
    data['Number of videos'] = len(list(webroot.glob('vids/**/*.*')))
    data['Number of HTML files'] = len(list(webroot.glob('*.html'))) + 1 # plus this one
    data['Total Lines of Code'] = count_lines_of_code(args.directory / 'src')
    data['Number of entries'] = len(entries)
    data['Timespan of entries'] = str((entries[0].date - entries[-1].date).days) + ' day(s)'

    oldest, newest = entries[-1], entries[0]
    data['Oldest entry'] = f'<a href="./{oldest.filename}">{oldest.title} - {oldest.description}</a>'
    data['Newest entry'] = f'<a href="./{newest.filename}">{newest.title} - {newest.description}</a>'

    longest, shortest = find_max_and_min_length(args.directory / 'entries', entries)
    data['Longest entry'] = f'<a href="./{longest.filename}">{longest.title} - {longest.description}</a>'
    data['Shortest entry'] = f'<a href="./{shortest.filename}">{shortest.title} - {shortest.description}</a>'

    content = utils.StringWriter(starting_indent=4)
    content.dl(data)

    page = utils.Page(
        filename='stats.html',
        title='Stats',
        description='Some interesting stats about this website.',
        banner=None
    )

    content = utils.render_page(
        page, full_url=args.full_url, content=content.text, nav_pages=nav, author=args.author,
    )

    with utils.write_page(args.directory, page.filename, overwrite_ok=args.overwrite) as f:
        f.write(content)
    logger.info('generated stats.html')
