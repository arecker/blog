import collections
import subprocess

GitChange = collections.namedtuple('GitChange', ['status', 'path'])

def git_status() -> list[GitChange]:
    output = subprocess.run('git status --short'.split(), check=True, capture_output=True)
    output = output.stdout.decode('UTF8').splitlines()
    changes = []
    for line in output:
        code, path = [k.strip() for k in line.split(' ')]
        status = {
            '??': 'untracked',
        }[code]
        change = GitChange(path=path, status=status)
        changes.append(change)
    return changes
