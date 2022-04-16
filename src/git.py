import collections
import logging
import subprocess

logger = logging.getLogger(__name__)

Commit = collections.namedtuple('Commit',
                                ['short_hash', 'long_hash', 'summary', 'url'])


def git_new_files(root_directory):
    cmd = 'git status --porcelain'.split(' ')
    result = subprocess.run(cmd,
                            cwd=root_directory,
                            capture_output=True,
                            check=True)
    lines = result.stdout.decode('UTF-8').splitlines()
    matches = [line[3:] for line in lines if line.startswith('?? ')]
    return [root_directory / m for m in matches]


def git_stage_all(root_directory):
    subprocess.run(['git', 'add', '-A'], cwd=root_directory, check=True)


def git_push_master(root_directory):
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
