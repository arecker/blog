# flake8: noqa

from .args import build_argparser
from .config import load_config
from .files import root_directory
from .info import gather_info
from .logger import configure_logging
from .page import Page
from .serve import start_web_server
from .xml import build_html_page

# iffy modules that depend on things
# from .git import fetch_git_info
# from .command import main, register_command
# from .page import Page
# from .serve import start_web_server
# from .test import load_tests, run_tests
