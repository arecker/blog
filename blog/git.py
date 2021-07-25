import collections
import subprocess

from . import root_directory

GitInfo = collections.namedtuple('GitInfo', 'head head_short summary')


def shell_command(cmd):
    result = subprocess.run(cmd.split(' '),
                            capture_output=True,
                            cwd=str(root_directory))

    return result.stdout.decode('UTF-8').strip()


def fetch_git_info() -> GitInfo:
    """Returns git information about the repo in the form of a named tuple.

    >>> info = fetch_git_info()
    >>> len(info.head_short)
    8
    """

    return GitInfo(
        shell_command('git rev-parse HEAD'),
        shell_command('git rev-parse --short HEAD'),
        shell_command('git log -1 --pretty=format:%s HEAD'),
    )
