import platform


class Site:
    """
    Website model.
    """

    def __init__(self):
        pass

    @property
    def python_version(self):
        """
        The python version used to build the website.

        ex. `v3.11.0`
        """
        return f'v{platform.python_version()}'
