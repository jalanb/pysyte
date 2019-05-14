"""Set up the pysyte project"""

import os
from setuptools import find_packages
from setuptools import setup

import pysyte

description = """Python modules often used in dotjab, and elsewhere

Available on guthub and pypi for ease of access
But probably not of great interest to others
"""

def package_files(directory):
    paths = []
    test_extensions = ('.test', '.tests')
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            extension = os.path.splitext(filename)[-1]
            if extension not in test_extensions:
                continue
            paths.append(os.path.join('..', path, filename))
    return paths

extra_files = package_files('pysyte')


setup(
    name=pysyte.__name__,
    packages=find_packages(),
    package_data={'': package_files('pysyte')},
    version=pysyte.__version__,
    url=f'https://github.com/jalanb/{pysyte.__name__}',
    download_url='https://github.com/jalanb/{pysyte.__name__}/tarball/v{pysyte.__version__}',
    license='MIT License',
    author='J Alan Brogan',
    author_email='github@al-got-rhythm.net',
    description=description.splitlines()[0],
    long_description=description,
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
        'inflect',
        'pprintpp',
        'path.py==7.7.1',
        'six',
        'stackprinter',
    ],
    scripts=[
        'bin/kat',
        'bin/short_dir',
        'bin/try',
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
    extras_require={
        'testing': ['nose'],
    }
)
