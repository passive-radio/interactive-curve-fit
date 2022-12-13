# Author: Yudai Okubo <yudaiokubo@gmail.com>
# Copyright (c) 2020-2022 Yudai Okubo
# License: MIT

from setuptools import setup

DESCRIPTION = "interactive_curve_fit: A Python project enables you to do curve fitting on spectrum data interactively on GUI. You can visualize your spectrum and fit the optional number of peaks on GUI using Scipy.optimize.curve_fit method."
NAME = 'interactive_curve_fit'
AUTHOR = 'Yudai Okubo'
AUTHOR_EMAIL = 'yudaiokubo@gmail.com'
URL = 'https://github.com/passive-radio/interactive-curve-fit'
LICENSE = 'MIT'
DOWNLOAD_URL = 'https://github.com/passive-radio/interactive-curve-fit'
VERSION = '0.0.2'
PYTHON_REQUIRES = '>=3.6'
KEYWORDS = 'curve fit spectrum'

INSTALL_REQUIRES = [
    'cycler==0.11.0',
    'fonttools==4.28.3',
    'kiwisolver==1.3.2',
    'matplotlib==3.5.0',
    'numpy==1.21.4',
    'packaging==21.3',
    'pandas==1.3.4',
    'Pillow==8.4.0',
    'pyparsing==3.0.6',
    'python-dateutil==2.8.2',
    'pytz==2021.3',
    'scipy==1.7.3',
    'setuptools-scm==6.3.2',
    'six==1.16.0',
    'tomli==1.2.2'
]

PACKAGES = [
    'interactive_curve_fit'
]

CLASSIFIERS = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]

with open('README.md', 'r', encoding='utf-8') as fp:
    readme = fp.read()

LONG_DESCRIPTION = readme
LONG_DESCRIPTION_CONTENT_TYPE = 'text/markdown'

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=AUTHOR,
    maintainer_email=AUTHOR_EMAIL,
    url=URL,
    download_url=URL,
    packages=PACKAGES,
    classifiers=CLASSIFIERS,
    license=LICENSE,
    keywords=KEYWORDS,
    install_requires=INSTALL_REQUIRES
)