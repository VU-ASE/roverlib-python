from setuptools import find_packages, setup

with open("lib/README.md", "r") as f:
    long_description = f.read()

setup(
    name="roverlib",
    version="0.0.25",
    description="An entrypoint library that provides full integration with the ASE software framework.An entrypoint library that provides full integration with the ASE software framework.",
    package_dir={"": "lib"},
    packages=find_packages(where="lib"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/VU-ASE/roverlib-python",
    author="Max Gallup",
    author_email="ase@vu.nl",
    license="GPL",
    classifiers=[
        "Framework :: Robot Framework :: Library",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3.10",
)
