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


setup(
    name=pysyte.__name__,
    version=pysyte.__version__,
    description=description.splitlines()[0],
    long_description=description,
    url='https://github.com/jalanb/%s' % pysyte.__name__,
    packages=find_packages(),
    package_data={'': package_files('pysyte')},
    download_url='https://github.com/jalanb/%s/tarball/v%s' % (
        pysyte.__name__, pysyte.__version__),
    license='MIT License',
    author='jalanb',
    author_email='github@al-got-rhythm.net',
    platforms='any',
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Build Tools',
    ],
    install_requires=[
        "boltons",
        "deprecated",
        "inflect<3.0.0",
        "path.py==7.7.1",
        "pyyaml",
        "sh",
        "stackprinter",
    ],
    test_requires=[
        "codecov",
        "coverage",
        "pytest",
        "pytest-cov",
    ],
    lint_requires=[
        "black",
        "flake8",
        "pylint",
    ],
    devops_requires=[
        "bumpversion",
    ],
    dev_requires=[
        "ipython",
        "pprintpp",
        "pudb",
        "pylint",
        "sh",
    ],
    scripts=[
        'bin/kat',
        'bin/getkey',
        'bin/short_dir',
        'bin/imports',
        'bin/rePATH',
        'bin/std',
    ],
)
