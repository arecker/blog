import re

from . import shell


r_status_short = re.compile(
    r'^(?P<glypph>\S+)\s+(?P<path>.*)$',
    flags=re.MULTILINE
)


def new_files():
    result = shell.run('git status --short')
    for glyph, path in r_status_short.findall(result.stdout):
        if glyph != 'D':
            yield path


def stage(filepath):
    shell.run(f'git add {filepath}')


def amend(commit='HEAD'):
    shell.run(f'git commit --amend -C {commit}')


def push(remote='origin', local_branch='master', remote_branch='master'):
    shell.run(f'git push origin {local_branch}:{remote_branch}')


def tag(name, push=True, remote='origin'):
    shell.run(f'git tag {name}')
    if push:
        shell.run(f'git push {remote} {name}')


def latest_tag():
    output = shell.run('git tag --sort version:refname').stdout
    return output.splitlines()[-1]


def shortlog_from_latest_tag():
    cmd = f'git shortlog {latest_tag()}..HEAD'
    return shell.run(cmd).stdout
