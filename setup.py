import os
import sys
from setuptools import setup

SETUP_VERSION = None
with open( 'VERSION.txt', 'r' ) as reader:
    SETUP_VERSION = reader.read()
# base="Win32GUI" should be used only for Windows GUI app
base = None
if sys.platform == "win32":
    base = "Win32GUI"

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "BlackBeard",
    version = SETUP_VERSION,
    author = "Mark McLarnon",
    author_email = "mark.mclarnon@gmail.com",
    description = ("A tool for interacting with GitHub"),
    license = "BSD",
    keywords = "example documentation tutorial",
    url = "http://packages.python.org/an_example_pypi_project",
    packages=['src'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)