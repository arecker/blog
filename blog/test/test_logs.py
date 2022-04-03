import contextlib
import logging
import pathlib
import unittest
import unittest.mock

from .. import logs


@contextlib.contextmanager
def patch_logging():
    logger = unittest.mock.Mock()
    with unittest.mock.patch.object(logging, 'getLogger', return_value=logger):
        yield logger


class TestLogs(unittest.TestCase):
    def test_prettify_log(self):
        with unittest.mock.patch.object(pathlib.Path,
                                        'home',
                                        return_value='/home/testy'):
            message = ('a bunch of files were written to '
                       '/home/testy/logs, '
                       'you should go check that out.')
            actual = logs.prettify_log(message)
            expected = ('a bunch of files were written to '
                        '~/logs, '
                        'you should go check that out.')

            self.assertEqual(actual, expected)

    def test_configure_logger(self):
        with patch_logging() as mock:
            logs.configure_logging()
            mock.setLevel.assert_called_once_with(logging.INFO)

        with patch_logging() as mock:
            logs.configure_logging(verbose=True)
            mock.setLevel.assert_called_once_with(logging.DEBUG)
