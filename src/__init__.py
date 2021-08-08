# flake8: noqa

from .args import build_argparser
from .config import load_config
from .info import build_global_context
from .logger import configure_logging
from .page import Page
from .serve import start_web_server
from .targets import pages_target_group, entries_target_group
from .xml import build_html_page, build_rss_feed

# iffy modules that depend on things
# from .git import fetch_git_info
# from .command import main, register_command
# from .page import Page
# from .serve import start_web_server
# from .test import load_tests, run_tests
