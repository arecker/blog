import collections
import re
import subprocess

GitChange = collections.namedtuple('GitChange', ['status', 'state', 'path'])


def git_status() -> list[GitChange]:
    output = subprocess.run('git status --short'.split(),
                            check=True,
                            capture_output=True).stdout.decode('utf-8')
    changes = [new_git_change(line.strip()) for line in output.splitlines()]
    return changes


p_git_change = re.compile(
    r'^(?P<key_1>[A-Z? ])(?P<key_2>[A-Z? ]) (?P<path>(.*?))$',
    flags=re.MULTILINE)


def new_git_change(git_status_output_line: str) -> GitChange:
    if match := p_git_change.match(git_status_output_line):
        first, second, path, _ = match.groups()

        if first == ' ' and second == 'M':
            return GitChange(status='untracked', state='modified', path=path)

        if first == second == '?':
            return GitChange(status='untracked', state='added', path=path)

        if first == 'M' and second == ' ':
            return GitChange(status='staged', state='modified', path=path)

        if first == 'A' and second == ' ':
            return GitChange(status='staged', state='added', path=path)

        raise ValueError(f'unknown status key: {git_status_output_line}')

    raise ValueError(
        f'can\'t parse status key and path: {git_status_output_line}')
