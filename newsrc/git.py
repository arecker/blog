from newsrc import shell


def head():
    return shell.command('git rev-parse HEAD')


def short_head():
    return shell.command('git rev-parse --short HEAD')


def head_summary():
    return shell.command(f'git log -1 --pretty=format:%s HEAD')
