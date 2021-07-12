from newsrc import shell


def head():
    return shell.shell_command('git rev-parse HEAD')


def short_head():
    return shell.shell_command('git rev-parse --short HEAD')


def head_summary():
    return shell.shell_command(f'git log -1 --pretty=format:%s HEAD')
