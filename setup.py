#!/usr/bin/env python

import distutils.core

distutils.core.setup(name='blog',
                     packages=['blog'],
                     entry_points={'console_scripts': [
                         'blog = blog:main',
                     ]})
