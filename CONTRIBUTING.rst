============
Contributing
============

Thanks for contributing to ``bluemvmt-gsf``.

Development setup
=================

This project uses Poetry for dependency management and packaging.

1. Install Poetry: https://python-poetry.org/docs/#installation
2. Clone the repository and install dependencies::

       git clone https://github.com/vincebluemvmt/bluemvmt-gsf.git
       cd bluemvmt-gsf
       poetry install --with dev,docs

3. Install git hooks::

       poetry run pre-commit install

Native libraries
================

Bundled shared libraries live under
``src/bluemvmt_gsf/libgsf/lib/``:

- ``libgsf-x86_64-03.11.so``
- ``libgsf-aarch64-03.11.so``

Only GSF 3.11 is supported. Rebuild or replace those files from the companion
JSON-enabled libgsf sources when updating the native layer. Do not reintroduce
older ``03.08`` / ``03.09`` / ``03.10`` binaries.

Making changes
==============

1. Create a branch from ``main``.
2. Make your changes with tests.
3. Format and lint::

       poetry run pre-commit run --all-files

4. Run tests::

       poetry run pytest

5. Open a pull request against
   https://github.com/vincebluemvmt/bluemvmt-gsf

Documentation
=============

Docs are written in reStructuredText and built with Sphinx::

    poetry run sphinx-build -b html docs docs/_build/html

Preview the HTML output by opening ``docs/_build/html/index.html``.

Reporting issues
================

Please include:

- Linux distribution and architecture (``x86_64`` or ``aarch64``)
- Python version
- ``bluemvmt-gsf`` version
- A minimal reproduction when possible

Issue tracker: https://github.com/vincebluemvmt/bluemvmt-gsf/issues

Releasing
=========

1. Update ``CHANGELOG.rst`` and the version in ``pyproject.toml``.
2. Tag a release (``vX.Y.Z`` or ``X.Y.Z``).
3. CI builds with Poetry, runs tests against the wheel, and publishes tagged
   releases to PyPI via trusted publishing.
