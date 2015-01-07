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
    entry_points = {
        'console_scripts': [
            'blog = blog.cli.main',
        ]
    }
)