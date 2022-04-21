import contextlib
import logging
import pathlib
import unittest
import unittest.mock

from .. import cli


@contextlib.contextmanager
def patch_logging():
    logger = unittest.mock.Mock()
    with unittest.mock.patch.object(logging, 'getLogger', return_value=logger):
        yield logger


class TestCLI(unittest.TestCase):
    def test_parse_args(self):
        verbose = cli.parse_args(['-v']).verbose
        self.assertTrue(verbose)
        debug = cli.parse_args(['-d']).debug
        self.assertTrue(debug)
        subcommand = cli.parse_args(['help']).subcommand
        self.assertEqual(subcommand, 'help')

    def test_prettify_log(self):
        with unittest.mock.patch.object(pathlib.Path,
                                        'home',
                                        return_value='/home/testy'):
            message = ('a bunch of files were written to '
                       '/home/testy/logs, '
                       'you should go check that out.')
            actual = cli.prettify_log(message)
            expected = ('a bunch of files were written to '
                        '~/logs, '
                        'you should go check that out.')

            self.assertEqual(actual, expected)

    def test_configure_logger(self):
        with patch_logging() as mock:
            cli.configure_logging()
            mock.setLevel.assert_called_once_with(logging.INFO)

        with patch_logging() as mock:
            cli.configure_logging(verbose=True)
            mock.setLevel.assert_called_once_with(logging.DEBUG)

    def test_register_command(self):
        with unittest.mock.patch.dict(cli.COMMANDS, {}) as p:

            @cli.register_command
            def mycmd(args):
                """Just some command."""

            cmd = p['mycmd']
            self.assertEqual(cmd.name, 'mycmd')
            self.assertEqual(cmd.docstring, 'Just some command.')
            self.assertEqual(cmd.function, mycmd)
