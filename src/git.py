import os
import subprocess


def git_new_files(root_directory=os.curdir):
    cmd = 'git status --porcelain'.split(' ')
    result = subprocess.run(cmd,
                            cwd=root_directory,
                            capture_output=True,
                            check=True)
    lines = result.stdout.decode('UTF-8').splitlines()
    matches = [line[3:] for line in lines if line.startswith('?? ')]
    return matches
