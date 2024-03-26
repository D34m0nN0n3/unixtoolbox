import json
from setuptools import setup, find_packages

# Load list of dependencies
with open("requirements.txt") as data:
    install_requires = [
        line for line in data.read().split("\n")
        if line and not line.startswith("#")
    ]

# Package description
setup(
    install_requires = install_requires,
)
