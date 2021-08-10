import logging
import os
import subprocess

logger = logging.getLogger(__name__)


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
                   check=True)


def git_write_tag(root_directory=os.curdir, tag=''):
    subprocess.run(['git', 'tag', tag], cwd=root_directory, check=True)


def git_push_master(root_directory=os.curdir):
    cmd = 'git push origin master:master'
    subprocess.run(cmd.split(' '), cwd=root_directory, check=True)


def git_push_tag(root_directory, tag=''):
    cmd = f'git push origin {tag}'
    subprocess.run(cmd.split(' '), cwd=root_directory, check=True)


def git_publish_entry(context):
    git_stage_all(context.root_directory)
    logger.debug('staged all files')

    message = f'entry: {context.latest.title}'
    git_write_commit(context.root_directory, message=message)
    logger.debug('wrote commit: %s', message)

    tag = f'entry-{context.latest.slug}'
    git_write_tag(context.root_directory, tag=tag)
    logger.debug('wrote tag %s', tag)

    git_push_tag(context.root_directory, tag=tag)
    logger.debug('pushed tag %s', tag)

    git_push_master(context.root_directory)
    logger.debug('successfully pushed repo')

    logger.info('successfully published %s (%s)', tag, message)
