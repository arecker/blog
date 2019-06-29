from setuptools import setup

setup(
    name='blog',
    version='0.1',
    description='My Blog, Man',
    url='http://github.com/arecker/blog',
    author='Alex Recker',
    author_email='alex@reckefamily.com',
    license='GPLV3',
    packages=['blog'],
    zip_safe=False,
    scripts=['bin/blog']
)
