#! /usr/bin/env python

from setuptools import setup

setup(name='pysemgen',
      version='0.1.0',
      description='Annotation software for SBML / CellML models',
      author='J. Kyle Medley',
      packages=['semgen'],
      package_data={'semgen': [
          'cache/chebi.json',
      ]},
      include_package_data=True,
      install_requires=[
        #'tellurium>=2.1.0',
        ],
      )
