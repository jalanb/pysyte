import os
from dataclasses import dataclass
import setuptools

import pysyte as project



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


description = """Pysyte extends Python

Available on github and pypi for ease of access
"""
headline = description.splitlines()[0]
name = project.__name__
version = project.__version__

@dataclass
class User:
    service: str
    username: str
    email: str
    name: str

    def url(self, name):
        return f'https://{self.service}/{self.username}/{name}'

user = User('github.com', 'jalanb', 'github@al-got-rhythm.net', 'J Alan Brogan')

setuptools.setup(
    name=name,
    version=version,
    description=headline,
    long_description=description,
    url=user.url(name),
    packages=setuptools.find_packages(),
    package_data={'': package_files('{name}')},
    download_url='{user.url(name)}/tarball/v{version}',
    license='MIT License',
    author=user.name,
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
        'inflect',
        'pprintpp',
        'path.py==7.7.1',
        'six',
        'stackprinter',
        'pyyaml',
        'boltons',
        'python-magic',
        'deprecated',
    ],
    # entry_points = {
    #     'console_scripts': [
    #         'kat = pysyte.cli.bin:kat'
    #     ]
    # },
    scripts=[
        'bin/kat',
        'bin/keys',
        'bin/short_dir',
        'bin/imports',
        'bin/rePATH',
        'bin/std',
    ],
)
