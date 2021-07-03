import newsrc as blog


@blog.command
def write():
    """
    run blog in local writing mode
    """
    # latest = blog.entries()[0]
    # latest.build()
    blog.serve()


@blog.command
def test():
    """
    run the unit tests
    """
    blog.run_tests()


@blog.command
def serve():
    """
    serve site locally
    """
    blog.serve()



if __name__ == '__main__':
    blog.main()
