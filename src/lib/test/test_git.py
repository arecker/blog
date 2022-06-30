import contextlib
import os
import pathlib
import subprocess
import tempfile
import unittest
import unittest.mock

from .. import git


@contextlib.contextmanager
def tmp_git_repo():
    cwd = os.curdir
    try:
        with tempfile.TemporaryDirectory() as tmp:
            os.chdir(tmp)
            subprocess.run('git init'.split(),
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL,
                           check=True)
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
            self.assertEqual(change.state, 'added')
            self.assertEqual(change.status, 'untracked')

            subprocess.run('git add -A'.split(),
                           check=True,
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)

            changes = git.git_status()
            self.assertEqual(len(changes), 1)
            change = changes[0]
            self.assertEqual(change.path, 'test.txt')
            self.assertEqual(change.state, 'added')
            self.assertEqual(change.status, 'staged')

            pathlib.Path('test2.txt').touch()
            changes = git.git_status()
            self.assertEqual(len(changes), 2)
            change = next((c for c in changes if c.status == 'untracked'))
            self.assertEqual(change.path, 'test2.txt')
            self.assertEqual(change.state, 'added')
            change = next((c for c in changes if c.status == 'staged'))
            self.assertEqual(change.path, 'test.txt')
            self.assertEqual(change.state, 'added')

            with pathlib.Path('test.txt').open('a') as f:
                f.write('more text')
            changes = git.git_status()
            self.assertEqual(len(changes), 2)
            change = [c for c in changes if c.path == 'test.txt']
            change = next((c for c in change if c.status == 'mixed'))
            self.assertEqual(change.state, 'mixed')
            change = next((c for c in changes if c.status == 'untracked'))
            self.assertEqual(change.state, 'added')

    def test_new_git_change(self):
        change = git.new_git_change(' M blog/__init__.py')
        self.assertEqual(change.path, 'blog/__init__.py')
        self.assertEqual(change.status, 'untracked')
        self.assertEqual(change.state, 'modified')

        change = git.new_git_change('?? www/images/test.jpg')
        self.assertEqual(change.path, 'www/images/test.jpg')
        self.assertEqual(change.status, 'untracked')
        self.assertEqual(change.state, 'added')

        change = git.new_git_change('M  www/images/test.jpg')
        self.assertEqual(change.path, 'www/images/test.jpg')
        self.assertEqual(change.status, 'staged')
        self.assertEqual(change.state, 'modified')

        change = git.new_git_change('A  www/images/test.jpg')
        self.assertEqual(change.path, 'www/images/test.jpg')
        self.assertEqual(change.status, 'staged')
        self.assertEqual(change.state, 'added')

        change = git.new_git_change('AM  www/images/test.jpg')
        self.assertEqual(change.path, 'www/images/test.jpg')
        self.assertEqual(change.status, 'mixed')
        self.assertEqual(change.state, 'mixed')

        change = git.new_git_change(' M Makefile')
        self.assertEqual(change.path, 'Makefile')
        self.assertEqual(change.status, 'untracked')
        self.assertEqual(change.state, 'modified')

        change = git.new_git_change('D  www/test-git-hook.jpg')
        self.assertEqual(change.state, 'deleted')
        self.assertEqual(change.status, 'staged')

        with self.assertRaisesRegex(ValueError, 'unknown status'):
            git.new_git_change('AD  www/blah.jpg')

        with self.assertRaisesRegex(ValueError, 'can\'t parse'):
            git.new_git_change('How did this happen?')

    def test_git_add(self):
        with tmp_git_repo():
            pathlib.Path('test.txt').touch()
            git.git_add('test.txt')
            changes = git.git_status()
            assert len(changes) == 1
            change = changes[0]
            self.assertEqual(change.status, 'staged')
            self.assertEqual(change.state, 'added')
