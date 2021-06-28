def count_list(arglist):
    """
    Iterate over a list, providing the total and current index of each
    item in arglist.
    """
    total = len(arglist)

    for current, thing in enumerate(arglist):
        yield thing, current + 1, total
