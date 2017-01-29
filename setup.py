import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "DockerMachine Windows API",
    version = "0.0.1",
    author = "Ashish Bhatiya",
    author_email = "ashishbhatiya18@gmail.com",
    description = ("A simple DockerMachine API for Windows Platform for creating and stopping containers"),
    license = "BSD",
    keywords = "docker docker-machine API",
    packages=['api'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
