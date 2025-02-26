from setuptools import setup, find_packages
from os import path
dir = path.abspath(path.dirname(__file__))

with open(path.join(dir, "README.md"), encoding="utf-8") as file:
    description = file.read()


setup(
    name="roverlib",
    version="0.0.1",
    url = "https://github.com/VU-ASE/roverlib-python",
    author="VU-ASE",
    long_description=description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
)