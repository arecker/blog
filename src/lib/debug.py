import code


def ipython_supported():
    try:
        import IPython
        return True
    except ImportError:
        return False


def interact():
    import lib
    import main

    if ipython_supported():
        print('launching console with ipython')
        import IPython
        IPython.embed()
    else:
        print('ipython missing, launching console with regular REPL')
        code.interact(local=globals())
