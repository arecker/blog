import collections
import datetime
import logging
import subprocess

logger = logging.getLogger(__name__)

Pages = collections.namedtuple('Pages', ['next', 'previous'])
GitInfo = collections.namedtuple('GitInfo',
                                 ['head', 'head_short', 'head_summary'])
Info = collections.namedtuple(
    'Info', ['timestamp', 'git', 'pagination', 'latest', 'entries'])


def shell_command(cmd):
    result = subprocess.run(cmd.split(' '), capture_output=True)
    return result.stdout.decode('UTF-8').strip()


def build_pagination_map(entries=[]) -> dict:
    pagination = {}

    for i, entry in enumerate(entries):
        if i > 0:
            previous_entry = entries[i - 1].filename
        else:
            previous_entry = None

        try:
            next_entry = entries[i + 1].filename
        except IndexError:
            next_entry = None

        pagination[entry.filename] = Pages(next_entry, previous_entry)

    return pagination


def gather_git_info() -> GitInfo:
    return GitInfo(
        head=shell_command('git rev-parse HEAD'),
        head_short=shell_command('git rev-parse --short HEAD'),
        head_summary=shell_command('git log -1 --pretty=format:%s HEAD'),
    )


def gather_info(entries=[]) -> Info:
    timestamp = datetime.datetime.now()
    logger.debug('created build timestamp %s', timestamp)

    git = gather_git_info()
    logger.debug('gathered git info %s', git)

    pagination = build_pagination_map(entries)
    logger.debug('built pagination map from %d entry file(s)', len(entries))

    latest = entries[-1]
    logger.debug('cached latest entry %s', latest)

    return Info(timestamp=timestamp,
                git=git,
                pagination=pagination,
                latest=latest,
                entries=entries)
