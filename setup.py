#!/usr/bin/env python
""" setup.py

"""
from setuptools import setup, find_packages
import bananabot

setup(
    name="bananabot",
    version=bananabot.VERSION,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click>=6.0', 'yapf>=0.17', 'requests>=0.0.1', 'PyYAML>=3.12'
    ],
    entry_points={
        'console_scripts': ['bananabot=bananabot.bananabot:bananabot'],
    },
    package_data={
        '': ['*.txt', '*.rst', '*.sh', 'LICENSE', '*md'],
        'bananabot': ['config.yaml'],
    },

    # metadata
    author="Jack Chang",
    author_email="wei0831@gmail.com",
    description="simple twitch chat bot",
    license="MIT",
    keywords="twitch, chat",
    url="",
    classifiers=[
        'Development Status :: 1 - Planning Development',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ], )
