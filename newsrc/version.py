import platform
import sys

from .files import join


with open(join('src/VERSION')) as f:
    version = f.read().strip()


python_version = platform.python_version()
python_executable = sys.executable
