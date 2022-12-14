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
VERSION = '0.0.0'
PYTHON_REQUIRES = '>=3.6'
KEYWORDS = 'curve fit spectrum'

INSTALL_REQUIRES = [
    'matplotlib>=3.5.0',
    'numpy>=1.21.4',
    'pandas>=1.3.4',
    'Pillow>=8.4.0',
    'scipy>=1.7.3',
]

PACKAGES = [
    'interactive_curve_fit', 'interactive_curve_fit/core', 'interactive_curve_fit/utils'
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