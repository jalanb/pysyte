"""Set up the dotsite project"""


from setuptools import setup


import dotsite


setup(
    name='dotsite',
    version=dotsite.__version__,
    url='https://github.com/jalanb/dotsite',
    license='MIT License',
    author='J Alan Brogan',
    author_email='dotsite@al-got-rhythm.net',
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
    test_suite='nose.collector',
    tests_require=['nose'],
    extras_require={
        'testing': ['nose'],
    }
)
