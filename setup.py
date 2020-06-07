from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="athom-api",
    version="1.0.0",
    author="Roy K",
    author_email="rkokk@protonmail.com",
    description=("A python module for accessing the Athom Web-API for use with the Athom Homey"),
    license="GPLv3",
    keywords="API athom homey",
    url="https://github.com/rkokkelk/python-athom-api",
    install_requires=[
        'configparser==3.5.0',
        'marshmallow==3.0.0rc1',
        'requests==2.21.0'
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=['contrib', 'docs', 'env*', 'tests*']),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Home Automation'
    ],
    entry_points={
        'console_scripts': [
            'athom = athom.__main__:main'
        ]
    }
)
