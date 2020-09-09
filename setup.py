"""Set up the pysyte project"""

import os
from setuptools import find_packages
from setuptools import setup

import pysyte

description = """Pysyte extends Python

Available on github and pypi for ease of access
"""


def package_files(directory):
    paths = []
    extensions = ('.test', '.tests', '.yaml')
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            extension = os.path.splitext(filename)[-1]
            if extension not in extensions:
                continue
            paths.append(os.path.join('..', path, filename))
    return paths


extra_files = package_files('pysyte')


package_data = {'': package_files('pysyte')},
setup(packages=find_packages())
