import subprocess

from newsrc.logger import logger
from newsrc.files import in_root

encoding = 'UTF-8'


def command(command):
    args = command.split()

    with in_root():
        result = subprocess.run(args, capture_output=True)

    template = '''
'shell command `%s` exited %d
------------------------------------------------------------------------
STDOUT:
%s
------------------------------------------------------------------------
STDERR:
%s
------------------------------------------------------------------------
'''.strip()

    logger.debug(template, args, result.returncode, result.stdout,
                 result.stderr)

    return result.stdout.decode(encoding).strip()
