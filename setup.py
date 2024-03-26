import sys
import json
from setuptools import setup, find_packages

sys.stderr.write(
    """
===============================
Unsupported installation method
===============================
This version of mkdocs-material no longer supports
installation with `python setup.py install`.
Please use `python -m pip install .` instead.
"""
)
sys.exit(1)

# Load list of dependencies
with open("requirements.txt") as data:
    install_requires = [
        line for line in data.read().split("\n")
        if line and not line.startswith("#")
    ]

# Package description
setup(
    name = "mkdocs-material",
    install_requires = install_requires,
)
