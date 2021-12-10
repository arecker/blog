import collections
import logging
import os
import subprocess

logger = logging.getLogger(__name__)

Commit = collections.namedtuple('Commit',
                                ['short_hash', 'long_hash', 'summary', 'url'])


def git_new_files(root_directory=os.curdir):
    cmd = 'git status --porcelain'.split(' ')
    result = subprocess.run(cmd,
                            cwd=root_directory,
                            capture_output=True,
                            check=True)
    lines = result.stdout.decode('UTF-8').splitlines()
    matches = [line[3:] for line in lines if line.startswith('?? ')]
    return [root_directory / m for m in matches]


def git_stage_all(root_directory=os.curdir):
    subprocess.run(['git', 'add', '-A'], cwd=root_directory, check=True)


def git_write_commit(root_directory=os.curdir, message=''):
    subprocess.run(['git', 'commit', '-m', message],
                   cwd=root_directory,
                   check=True,
                   stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)


def git_write_tag(root_directory=os.curdir, tag=''):
    subprocess.run(['git', 'tag', tag],
                   cwd=root_directory,
                   check=True,
                   stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)


def git_push_master(root_directory=os.curdir):
    cmd = 'git push origin master:master'
    subprocess.run(cmd.split(' '),
                   cwd=root_directory,
                   check=True,
                   stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)


def git_push_tag(root_directory, tag=''):
    cmd = f'git push origin {tag}'
    subprocess.run(cmd.split(' '),
                   cwd=root_directory,
                   check=True,
                   stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)


def get_head_commit(root_directory):
    def shell_command(cmd):
        result = subprocess.run(cmd.split(' '), capture_output=True)
        return result.stdout.decode('UTF-8').strip()

    long_hash = shell_command('git rev-parse HEAD')

    return Commit(short_hash=shell_command('git rev-parse --short HEAD'),
                  long_hash=long_hash,
                  summary=shell_command('git log -1 --pretty=format:%s HEAD'),
                  url=f'https://github.com/arecker/blog/commit/{long_hash}')


def head_is_entry_tagged(root_directory):
    cmd = 'git describe --exact-match --tags HEAD'
    result = subprocess.run(cmd.split(' '),
                            cwd=root_directory,
                            capture_output=True,
                            check=False)

    if result.returncode != 0:  # HEAD isn't tagged
        return False

    output = result.stdout.decode('UTF-8').strip()
    return output.startswith('entry-')
