import os
from setuptools import setup


def read(fname):
    """
    Utility function to read the README file.
    Used for the long_description.  It's nice, because now 1) we have a top
    level README file and 2) it's easier to type in the README file than to put
    a raw string in below ...
    """
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setup(
    name="jinjamagic",
    version="0.1.0",
    author="Tony Fast",
    author_email="tony.fast@continuum.io",
    description="Literate Python Programming with Markdown Template Magic ",
    license="BSD",
    keywords="IPython markdown commonmark jinja2 template Jupyter",
    url="http://github.com/ContinuumIO/jinjamagic",
    packages=["jinjamagic"],
    long_description=read("README.md"),
    classifiers=[
        "Topic :: Utilities",
        "Framework :: IPython",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Topic :: Software Development :: Testing",
    ],
    include_package_data=True
)
