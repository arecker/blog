import newsrc as blog


@blog.command
def write():
    """
    run blog in local writing mode
    """
    blog.serve()


@blog.command
def test():
    """
    run the unit tests
    """
    blog.run_tests()



if __name__ == '__main__':
    blog.main()
