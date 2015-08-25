from setuptools import setup, find_packages
from urlman import __version__

setup(
    name='urlman',
    version=__version__,
    description='Django URL pattern helpers',
    packages=find_packages(),
    author='Andrew Godwin',
    author_email='andrew@aeracode.org',
)

