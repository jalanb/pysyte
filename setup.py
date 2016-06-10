"""Set up the dotsite project"""


from setuptools import setup


import dotsite as site


name = 'dotsite'


setup(
    name=name,
    packages=[name],
    version=site.__version__,
    url='https://github.com/jalanb/dotsite',
    download_url=
        'https://github.com/jalanb/dotsite/tarball/v%s' % site.__version__,
    license='MIT License',
    author='J Alan Brogan',
    author_email='github@al-got-rhythm.net',
    description=site.__doc__,
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
    install_requires=['path.py'],
    test_suite='nose.collector',
    tests_require=['nose'],
    extras_require={
        'testing': ['nose'],
    }
)
