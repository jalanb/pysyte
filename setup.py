"""Set up the pysyte project"""


from setuptools import setup

import pysyte

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
    description=pysyte.__doc__,
    platforms='any',
    classifiers=[
        'Programming Language :: Python :: 2.7',
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
        'pdir',
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
