from setuptools import setup, find_packages
from urlman import __version__

setup(
    name='urlman',
    version=__version__,
    description='Django URL pattern helpers',
    url='https://github.com/andrewgodwin/urlman',
    packages=find_packages(),
    author='Andrew Godwin',
    author_email='andrew@aeracode.org',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
    ],
)
