import collections
import datetime
import logging
import subprocess

logger = logging.getLogger(__name__)

Info = collections.namedtuple(
    'Info', ['git_head', 'git_head_short', 'git_head_summary', 'timestamp'])


def shell_command(cmd):
    result = subprocess.run(cmd.split(' '), capture_output=True)
    return result.stdout.decode('UTF-8').strip()


def gather_build_info() -> Info:
    info = Info(shell_command('git rev-parse HEAD'),
                shell_command('git rev-parse --short HEAD'),
                shell_command('git log -1 --pretty=format:%s HEAD'),
                datetime.datetime.now())
    logger.debug('generated build info %s', info)
    return info
