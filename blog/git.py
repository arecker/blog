import pathlib
import subprocess


def git_new_files() -> list[pathlib.Path]:
    """Return all new files not yet staged in git."""

    cwd = str(pathlib.Path(__file__).parent.absolute())
    cmd = 'git status --porcelain'.split(' ')
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, check=True)
    lines = result.stdout.decode('UTF-8').splitlines()
    matches = [line[3:] for line in lines if line.startswith('?? ')]
    paths = [pathlib.Path(m) for m in sorted(matches)]
    return [p for p in paths if p.is_file()]
