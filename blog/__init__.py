# flake8: noqa

# pure modules (mo dependencies)
from .logger import logger
from .files import root_directory

# iffy modules that depend on things
from .command import main, register_command
from .page import Page
from .serve import start_web_server
from .test import run_tests