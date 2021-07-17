# tri-again

[![version](https://img.shields.io/pypi/v/tri-again?style=flat-square)][pypi]
[![python versions](https://img.shields.io/pypi/pyversions/tri-again?style=flat-square)][pypi]
[![license](https://img.shields.io/pypi/l/tri-again?style=flat-square)][pypi]
[![coverage](https://img.shields.io/badge/coverage-100%25-brightgreen?style=flat-square)][coverage]
[![build](https://img.shields.io/circleci/project/github/lace/tri-again/main?style=flat-square)][build]
[![code style](https://img.shields.io/badge/code%20style-black-black?style=flat-square)][black]

Simple scenegraph for quickly debugging 3D meshes, polylines, and points.

[pypi]: https://pypi.org/project/tri-again/
[coverage]: https://github.com/lace/tri-again/blob/main/.coveragerc#L2
[build]: https://circleci.com/gh/lace/tri-again/tree/main
[docs build]: https://tri-again.readthedocs.io/en/latest/
[black]: https://black.readthedocs.io/en/stable/


## Development

First, install Python 3.7 or 3.8 ([3.9 is not supported][issue 25]) and
[Poetry][install poetry].

After cloning the repo, run `./bootstrap.zsh` to initialize a virtual
environment with the project's dependencies.

Subsequently, run `./dev.py install` to update the dependencies.

[issue 25]: https://github.com/lace/tri-again/issues/25
[install poetry]: https://python-poetry.org/docs/#installation


## License

The project is licensed under the MIT license.
