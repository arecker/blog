import blog


@blog.register_command
def build(args):
    """Build the website locally"""


def main():
    blog.main()


if __name__ == '__main__':
    main()
