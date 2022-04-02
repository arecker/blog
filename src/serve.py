"""Serve webroot locally"""

import blog
import collections
import http.server
import logging
import pathlib
import threading
import time

from . import build, utils, games, entries as entries_cmd, archives, index

logger = logging.getLogger(__name__)


def start_web_server(webroot, port=8000):
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=webroot, **kwargs)

        def log_message(self, format, *args):
            logger.debug(f'{format}', *args)

    httpd = http.server.HTTPServer(('', port), Handler)
    try:
        logger.info('starting webserver at %s - http://0.0.0.0:%d',
                    utils.prettify_path(webroot), port)
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info('stopping web server')
        httpd.server_close()


def scan_files(directory: pathlib.Path, globs: list):
    for glob in globs:
        for f in directory.glob(glob):
            if blog.is_not_junk_file(f):
                yield f.absolute()


Snapshot = collections.namedtuple('Snapshot', ['path', 'mtime', 'keyword'])


def make_snapshot_list(directory: pathlib.Path):
    snapshots = []

    globs = [
        'data/*.json',
        'entries/*.html',
        'games/*.html',
    ]

    for f in scan_files(directory, globs):
        snapshot = {'path': f, 'mtime': f.stat().st_mtime}
        if f.parent.name == 'data':
            snapshot['keyword'] = f.stem
        elif f.parent.name == 'entries':
            snapshot['keyword'] = 'entries'
        elif f.parent.name == 'games':
            snapshot['keyword'] = 'games'
        else:
            raise ValueError(f'no known keyword for {utils.prettify_path(f)}')

        snapshots.append(Snapshot(**snapshot))

    return sorted(snapshots, key=lambda s: str(s))


def diff_snapshots(old_state: list[Snapshot],
                   new_state: list[Snapshot]) -> list[Snapshot]:
    for old_snapshot in old_state:
        try:
            new_snapshot = next(
                (s for s in new_state if s.path == old_snapshot.path))
            if old_snapshot.mtime != new_snapshot.mtime:
                logger.info('detected changed file %s',
                            utils.prettify_path(new_snapshot.path))
                yield old_snapshot
        except StopIteration:
            logger.info('detected deleted file %s',
                        utils.prettify_path(new_snapshot.path))
            yield new_snapshot

    for new_snapshot in new_state:
        try:
            next((s for s in old_state if s.path == new_snapshot.path))
        except StopIteration:
            logger.info('detected new file %s',
                        utils.prettify_path(new_snapshot.path))
            yield new_snapshot


Changeset = collections.namedtuple('Changeset', [
    'announcements',
    'entries',
    'games',
    'index',
    'nav',
])


def make_changeset(old_state: list[Snapshot],
                   new_state: list[Snapshot]) -> Changeset:
    changeset = {
        'announcements': False,
        'entries': False,
        'games': False,
        'index': False,
        'nav': False,
    }

    for snapshot in diff_snapshots(old_state, new_state):
        if snapshot.keyword == 'nav':
            changeset['nav'] = True
            changeset['entries'] = True
            changeset['games'] = True
            changeset['announcements'] = True
        if snapshot.keyword == 'games':
            changeset['games'] = True
        if snapshot.keyword == 'entries':
            changeset['entries'] = True

    return Changeset(**changeset)


def main(args):
    nav = utils.read_nav(args.directory / 'data')
    entries = blog.all_entries(args.directory)
    build.main(args, nav=nav, entries=entries)

    server_thread = threading.Thread(target=start_web_server,
                                     args=[args.directory / 'www'],
                                     daemon=True)
    server_thread.start()

    last_state = make_snapshot_list(args.directory)

    while True:
        time.sleep(1)

        current_state = make_snapshot_list(args.directory)
        changeset = make_changeset(last_state, current_state)

        if changeset.nav:
            nav = utils.read_nav(args.directory / 'nav.json')

        if changeset.entries:
            entries = blog.all_entries(args.directory)
            entries_cmd.main(args, nav=nav, entries=entries)
            archives.main(args, nav=nav, entries=entries)

        if changeset.games:
            games.main(args, nav=nav)

        if changeset.announcements or changeset.entries:
            index.main(args, nav=nav, entries=entries)

        last_state = current_state
