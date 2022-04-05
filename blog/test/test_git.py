import contextlib
import os
import pathlib
import subprocess
import tempfile
import unittest

from .. import git


@contextlib.contextmanager
def tmp_git_repo():
    cwd = os.curdir
    try:
        with tempfile.TemporaryDirectory() as tmp:
            os.chdir(tmp)
            subprocess.run('git init'.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            yield
    finally:
        os.chdir(cwd)
        

class TestGit(unittest.TestCase):
    def test_git_status(self):
        with tmp_git_repo():
            pathlib.Path('test.txt').touch()
            changes = git.git_status()
        self.assertEqual(len(changes), 1)
        change = changes[0]
        self.assertEqual(change.path, 'test.txt')
        self.assertEqual(change.status, 'untracked')
