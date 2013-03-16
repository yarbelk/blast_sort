#!/usr/bin/env python
#encoding: utf-8

from distutils.core import setup

setup(name="blast_sort",
        version='0.1',
        description='a utility to sort blasts of various species based on a lookup table',
        author='James Rivett-Carnac',
        author_email='james.rivettcarnac@gmail.com',
        packages=['blast_sort',],
        requires=['path.py',],
        scripts=['scripts/blast_sort',],
        )
