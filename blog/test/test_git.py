import contextlib
import subprocess
import unittest
import unittest.mock

from blog import git


@contextlib.contextmanager
def patch_run(output):
    result = unittest.mock.Mock(stdout=output.encode('utf-8'))
    with unittest.mock.patch.object(subprocess, 'run', return_value=result):
        yield


class TestGit(unittest.TestCase):
    def test_git_new_files(self):
        output = '''
 M blog/__init__.py
?? blog/git.py
?? blog/test/test_git.py
?? scripts/
'''.rstrip()

        with patch_run(output):
            files = git.git_new_files()
            self.assertEqual([f.name for f in files],
                             ['git.py', 'test_git.py'])
