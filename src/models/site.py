import argparse
import datetime
import os
import platform


class Site:
    """
    Website model.
    """

    def __init__(self, title='', description='', author='', email='', protocol='', domain='', timestamp=None):  # noqa: E501

        # site metadata
        self._title = title
        self._description = description
        self._author = author
        self._email = email

        # site URL
        self._protocol = protocol
        self._domain = domain

        # timestamp
        self._timestamp = timestamp

    @property
    def title(self) -> str:
        """
        Website title (ex `"Blog"`)
        """
        return self._title

    @property
    def description(self) -> str:
        """
        Website description (ex `"A Place for my Thoughts"`)
        """
        return self._description

    @property
    def author(self) -> str:
        """
        Website maintainer's full name.
        """
        return self._author

    @property
    def email(self) -> str:
        """
        Website maintainer's email.
        """
        return self._email

    @property
    def url(self) -> str:
        """
        Full website URL (ex. `"https://www.alexrecker.com"`)
        """
        return f'{self._protocol}://{self._domain}'

    @property
    def timestamp(self) -> datetime.datetime:
        """
        Website build timestamp.
        """
        return self._timestamp

    @property
    def python_version(self) -> str:
        """
        The python version used to build the website. (ex. `"v3.11.0")
        """
        return f'v{platform.python_version()}'


def load_site(args: argparse.Namespace) -> Site:
    """
    Creates a `Site` from the results of `parser.parse_args()`.

    ```python
    args = parser.parse_args()
    site = src.load_site(args)
    ```

    Will automatically supply all the args that start with `site_` to
    the constructor.

    Note: the timezone is hard-coded to `"America/Chicago"`
    (because nobody ever brags about the beef sandwich they had in
    Greenwich).
    """
    site_args = {k[5:]: v for k, v in vars(
        args).items() if k.startswith('site_')}

    # set timestamp
    os.environ['TZ'] = 'America/Chicago'
    timestamp = datetime.datetime.now()

    return Site(timestamp=timestamp, **site_args)
