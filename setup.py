#!/usr/bin/env python
#encoding: utf-8

from setuptools import setup

setup(name="query_contig_sort",
        version='0.1.4',
        description='a utility to sort blasts of various species for local blast with the fasta names all begining with Query_contig_',
        author='James Rivett-Carnac',
        author_email='james.rivettcarnac@gmail.com',
        packages=['query_contig_sort',],
        install_requires=['path.py',],
        scripts=['scripts/query_contig_sort',],
        test_suite= 'nose.collector',
        test_requires = ['nose',]
        )
