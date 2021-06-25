def count(arglist):
    total = len(arglist)
    for current, thing in enumerate(arglist):
        yield thing, current + 1, total
