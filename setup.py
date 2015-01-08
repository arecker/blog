from setuptools import setup

setup(
    name='Blog',
    version='4.0',
    description='My blog, man.',
    author='Alex Recker',
    author_email='alex@reckerfamily.com',
    url='http://alexrecker.com',
    packages=['blog'],
    license='GPL',

    install_requires = [
        "jinja2",
        "Markdown",
        "slugify",
        "beautifulsoup4",
        "click",
        "PyRSS2Gen",
        "flask",
        "requests",
        "tabulate"
    ],

    test_requires = [
      "nose"
    ],

    entry_points = {
        'console_scripts': [
            'blog = blog.cli:main',
        ]
    }
)