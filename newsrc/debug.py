import code

from .logger import info


def launch_console():
    import newsrc as blog

    try:
        import IPython
        info('launching ipython console')
        IPython.embed()
    except ImportError:
        info('launching python console')
        code.interact(local=globals())
