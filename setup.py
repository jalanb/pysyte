"""Set up the pysyte project"""


from setuptools import setup

import pysyte

description = """Python modules often used in dotjab, and elsewhere

Available on guthub and pypi for ease of access
But probably not of great interest to others
"""

setup(
    name=pysyte.__name__,
    packages=[pysyte.__name__],
    version=pysyte.__version__,
    url='https://github.com/jalanb/%s' % pysyte.__name__,
    download_url='https://github.com/jalanb/%s/tarball/v%s' % (
        pysyte.__name__, pysyte.__version__),
    license='MIT License',
    author='J Alan Brogan',
    author_email='github@al-got-rhythm.net',
    description=description.splitlines[0],
    long_description=description,
    platforms='any',
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Development Status :: 1 - Planning',
        'Natural Language :: English',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Build Tools',
    ],
    install_requires=[
        'nose==1.3.7',
        'pprintpp',
        'path.py==7.7.1',
    ],
    scripts=[
        'bin/kat',
        'bin/try',
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
    extras_require={
        'testing': ['nose'],
    }
)
