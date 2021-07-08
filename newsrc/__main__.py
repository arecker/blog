import json

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
    page = blog.whatever_type_by_file(blog.join(source))
    data = json.dumps(page.context, indent=2, sort_keys=True)
    blog.logger.info('rendering context for %s', page)
    print(data)


@blog.command
def render(source):
    """
    render a page as HTML
    """
    page = blog.whatever_type_by_file(blog.join(source))
    blog.logger.info('rendering %s as HTML', page)
    print(page.render())


if __name__ == '__main__':
    blog.main()
