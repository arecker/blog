"""Launch an interactive shell"""

import importlib
import logging
import pathlib

logger = logging.getLogger(__name__)


def main(args):
    src = importlib.import_module('.',
                                  package=pathlib.Path(__file__).parent.name)
    try:
        import IPython
        IPython.embed()
    except ImportError:
        logger.warn('ipython not found, falling back to a regular python REPL')
        import code
        code.InteractiveConsole(locals={'src': src}).interact()
