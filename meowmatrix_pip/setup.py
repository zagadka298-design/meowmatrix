from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="meowmatrix",
    version="2.0.0",
    description="A cmatrix alternative with multi-color mixing and rainbow mode",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zagadka298-design/meowmatrix",
    author="zagadka298",
    license="MIT",
    packages=["meowmatrix"],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "meowmatrix=meowmatrix:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Terminals",
    ],
)
