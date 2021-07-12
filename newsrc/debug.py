import code

from newsrc import logger


def launch_console():
    import newsrc as blog

    try:
        import IPython
        logger.info('launching ipython console')
        IPython.embed()
    except ImportError:
        logger.info('launching python console')
        code.interact(local=globals())


def set_trace_callback():
    try:
        import ipdb as pdb
    except ImportError:
        import pdb

    return pdb.set_trace
