#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()

readme = open("README.md").read()
doclink = """
Documentation
-------------

The full documentation is at http://complexitygraph.rtfd.org."""


setup(
    name="complexitygraph",
    version="0.1.0",
    description="Simple plots of the time complexity of a function using timeit.",
    long_description=readme + "\n\n" + doclink + "\n\n",
    author="John H. Williamson",
    author_email="johnhw@gmail.com",
    url="https://github.com/johnhw/complexitygraph",
    packages=["complexitygraph",],
    package_dir={"complexitygraph": "complexitygraph"},
    include_package_data=True,
    install_requires=[],
    license="MIT",
    zip_safe=False,
    keywords="complexitygraph",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
