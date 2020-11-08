import collections
import logging
import subprocess


logger = logging.getLogger('blog')


ShellResult = collections.namedtuple('ShellResult', 'code stdout stderr')


class ShellError(Exception):
    pass


def which(cmd):
    command = f'which {cmd}'
    return run(command, raise_on_exit=False).code == 0


def result_to_string(cmd, result):
    msg = '''command `{cmd}` returned {result.code}'''.format(
        cmd=cmd, result=result
    ) + '\n'

    output_fmt = '''
------------------------------ {label}
{output}
------------------------------
'''.strip() + '\n'

    if result.stdout:
        msg += output_fmt.format(label='stderr', output=result.stdout)
    if result.stderr:
        msg += output_fmt.format(label='stderr', output=result.stderr)

    return msg


def run(cmd, raise_on_exit=True):
    process = subprocess.Popen(
        cmd.split(' '),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = [str(s, 'utf-8').strip() for s in process.communicate()]
    result = ShellResult(process.returncode, stdout, stderr)
    msg = result_to_string(cmd, result)

    if raise_on_exit and result.code != 0:
        logger.error(msg)
        raise ShellError(f'The command `{cmd}` returned {result.code}')
    else:
        logger.debug(msg)

    return result
