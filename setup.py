import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), "README.rst")) as fh:
    readme_content = fh.read()

setup(
    name="urlman",
    version="2.0.1",
    description="Django URL pattern helpers",
    long_description=readme_content,
    url="https://github.com/andrewgodwin/urlman",
    packages=["urlman"],
    author="Andrew Godwin",
    author_email="andrew@aeracode.org",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: OS Independent",
    ],
)
