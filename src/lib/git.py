import collections
import logging
import re
import subprocess

logger = logging.getLogger(__name__)

GitChange = collections.namedtuple('GitChange', ['status', 'state', 'path'])


def git_status() -> list[GitChange]:
    output = subprocess.run('git status --short'.split(),
                            check=True,
                            capture_output=True).stdout.decode('utf-8')
    changes = [new_git_change(line.rstrip()) for line in output.splitlines()]
    return changes


p_git_change = re.compile(
    r'^(?P<key_1>[A-Z? ])(?P<key_2>[A-Z? ])\s+(?P<path>(.*?))$',
    flags=re.MULTILINE)


def git_push_tags():
    cmd = f'git push origin --tags'.split()
    logger.debug('running command %s', cmd)
    subprocess.run(cmd,
                   check=True,
                   stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)


def git_push_branch(branch):
    cmd = f'git push orgin {branch}:{branch}'.split()
    logger.debug('running command %s', cmd)
    subprocess.run(cmd,
                   check=True,
                   shell=True,
                   stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)


def git_add(path: str):
    cmd = f'git add {path}'.split()
    logger.debug('running command %s', cmd)
    subprocess.run(cmd,
                   check=True,
                   stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)


def git_commit(message: str):
    cmd = 'git commit -m'.split() + [message]
    logger.debug('running command %s', cmd)
    subprocess.run(cmd,
                   check=True,
                   stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)


def git_tag(tag: str):
    assert len(tag.split(' ')) == 1, "tag can't have spaces!"
    cmd = f'git tag {tag}'.split()
    logger.debug('running command %s', cmd)
    subprocess.run(cmd,
                   check=True,
                   stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)


def git_latest_tag():
    cmd = 'git describe --exact-match --tags HEAD'
    result = subprocess.run(cmd.split(' '), capture_output=True, check=False)

    if result.returncode != 0:  # HEAD isn't tagged
        return None

    return result.stdout.decode('UTF-8').strip()


def new_git_change(git_status_output_line: str) -> GitChange:
    if match := p_git_change.match(git_status_output_line):
        first, second, path, _ = match.groups()

        if first == ' ' and second == 'M':
            return GitChange(status='untracked', state='modified', path=path)

        if first == second == '?':
            return GitChange(status='untracked', state='added', path=path)

        if first == 'M' and second == ' ':
            return GitChange(status='staged', state='modified', path=path)

        if first == 'D' and second == ' ':
            return GitChange(status='staged', state='deleted', path=path)

        if first == 'A' and second == ' ':
            return GitChange(status='staged', state='added', path=path)

        if first == 'A' and second == 'M':
            return GitChange(status='mixed', state='mixed', path=path)

        if first == 'R' and second == ' ':
            return GitChange(status='staged', state='renamed', path=path)

        raise ValueError(f'unknown status key: {git_status_output_line}')

    raise ValueError(
        f'can\'t parse status key and path: {git_status_output_line}')
