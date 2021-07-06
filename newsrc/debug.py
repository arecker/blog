import code

from .logger import logger as l


def launch_console():
    import newsrc as blog

    try:
        import IPython
        l.info('launching ipython console')
        IPython.embed()
    except ImportError:
        l.info('launching python console')
        code.interact(local=globals())


def set_trace():
    try:
        import ipdb as pdb
    except ImportError:
        import pdb

    pdb.set_trace()
