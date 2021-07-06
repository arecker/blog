import newsrc as blog


@blog.command
def write():
    """
    run blog in local writing mode
    """
    # build pages
    for page in blog.pages():
        page.build()

    # build latest entry
    latest = blog.entries()[0]
    latest.build()
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


@blog.command
def shell():
    """
    launch interactive python shell
    """
    blog.launch_console()


@blog.command
def context(source):
    """
    show the context injected into a page
    """
    from pprint import pprint

    page = blog.page.Page(source)

    blog.info('{page}.context:')
    pprint(page.context)


if __name__ == '__main__':
    blog.main()
