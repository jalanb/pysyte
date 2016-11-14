"""Set up the dotsite project"""


import os
from setuptools import setup


import dotsite


p = os.path.join(os.path.dirname(__file__), 'requirements.txt')
with open(p) as stream:
    required = stream.read().splitlines()


setup(
    name=dotsite.__name__,
    packages=[dotsite.__name__],
    version=dotsite.__version__,
    url='https://github.com/jalanb/%s' % dotsite.__name__,
    download_url='https://github.com/jalanb/%s/tarball/v%s' % (
        dotsite.__name__, dotsite.__version__),
    license='MIT License',
    author='J Alan Brogan',
    author_email='github@al-got-rhythm.net',
    description=dotsite.__doc__,
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
    install_requires=required,
    test_suite='nose.collector',
    tests_require=['nose'],
    extras_require={
        'testing': ['nose'],
    }
)
