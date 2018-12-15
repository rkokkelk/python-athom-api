from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setup(
    name="python-athom-api",
    version="0.0.1",
    author="Roy K",
    author_email="rkokk@protonmail.com",
    description=("A python module for accessing the Athom Web-API for use with Athom Homey"),
    license="GPLv3",
    keywords="API athom homey",
    url="https://github.com/rkokkelk/python-athom-api",
    install_requires=requirements,
    long_description=long_description,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities"
    ]
)
