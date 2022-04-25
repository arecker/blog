import contextlib
import logging
import pathlib
import sys
import unittest
import unittest.mock
import urllib.parse

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

        args = cli.parse_args(['help'])
        self.assertIsInstance(args.dir_www, pathlib.Path)
        self.assertIsInstance(args.dir_entries, pathlib.Path)
        self.assertIsInstance(args.site_url, urllib.parse.ParseResult)
        self.assertIsInstance(args.site_year, int)

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


class TestMain(unittest.TestCase):
    def setUp(self):
        self.configure_logging = unittest.mock.Mock(name='configure_logging')
        unittest.mock.patch.object(cli,
                                   'configure_logging',
                                   new=self.configure_logging).start()

        self.logger = unittest.mock.Mock(name='logger')
        unittest.mock.patch.object(cli, 'logger', new=self.logger).start()

        self.sys_exit = unittest.mock.Mock(name='sys_exit')
        unittest.mock.patch.object(sys, 'exit', new=self.sys_exit).start()

        self.print_help = unittest.mock.Mock(name='print_help')
        unittest.mock.patch.object(cli.parser,
                                   'print_help',
                                   new=self.print_help).start()

    def reset_mocks(self):
        for mock in [
                self.print_help, self.sys_exit, self.logger,
                self.configure_logging
        ]:
            mock.reset_mock()

    def test_main(self):
        cli.main([])
        self.configure_logging.assert_called_once_with(verbose=False)
        self.sys_exit.assert_called_once_with(1)
        self.reset_mocks()

        cli.main(['-v', 'help'])
        self.configure_logging.assert_called_once_with(verbose=True)
        self.sys_exit.assert_called_once_with(0)
        self.print_help.assert_called_once()
        self.reset_mocks()

        mock_function = unittest.mock.Mock(name='mock function')
        mock_command = cli.Command(name='mycmd',
                                   docstring='some command',
                                   function=mock_function)
        commands = {'mycmd': mock_command}
        with unittest.mock.patch.object(cli, 'COMMANDS', new=commands):
            cli.main(['mycmd'])
            mock_function.assert_called_once()
            mock_function.reset_mock()
            self.reset_mocks()

            with unittest.mock.patch.object(cli.pdb, 'runcall') as p:
                cli.main(['-d', 'mycmd'])
                p.assert_called_once()

    def tearDown(self):
        unittest.mock.patch.stopall()
