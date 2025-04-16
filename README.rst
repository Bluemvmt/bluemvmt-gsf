.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

    .. image:: https://readthedocs.org/projects/bluemvmt-gsf/badge/?version=latest
        :alt: ReadTheDocs
        :target: https://bluemvmt-gsf.readthedocs.io/en/stable/
    .. image:: https://img.shields.io/coveralls/github/<USER>/bluemvmt-gsf/main.svg
        :alt: Coveralls
        :target: https://coveralls.io/r/<USER>/bluemvmt-gsf
    .. image:: https://img.shields.io/pypi/v/bluemvmt-gsf.svg
        :alt: PyPI-Server
        :target: https://pypi.org/project/bluemvmt-gsf/
    .. image:: https://img.shields.io/conda/vn/conda-forge/bluemvmt-gsf.svg
        :alt: Conda-Forge
        :target: https://anaconda.org/conda-forge/bluemvmt-gsf
    .. image:: https://pepy.tech/badge/bluemvmt-gsf/month
        :alt: Monthly Downloads
        :target: https://pepy.tech/project/bluemvmt-gsf
    .. image:: https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter
        :alt: Twitter
        :target: https://twitter.com/bluemvmt-gsf

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/
.. image:: https://coveralls.io/repos/github/vincebluemvmt/bluemvmt-gsf/badge.svg?branch=refs/tags/0.1.0
    :target: https://coveralls.io/github/vincebluemvmt/bluemvmt-gsf?branch=refs/tags/0.1.0
.. image:: https://github.com/vincebluemvmt/bluemvmt-gsf/actions/workflows/ci.yml/badge.svg
    :alt: Build Status
    :target: https://github.com/vincebluemvmt/bluemvmt-gsf/actions/workflows/ci.yml

|

============
bluemvmt-gsf
============


    Generic Sensor Format decoder to pure Python objects/types.


The gsfpy Python package is a simple ctype wrapper for the native C
libgsf library and is awkward to use.  The bluemvmt-gsf package adds
a layer to output pure Python Pydantic objects and pure Python types
that are much easier to use from your python code.



.. _pyscaffold-notes:

Making Changes & Contributing
=============================

This project uses `pre-commit`_, please make sure to install it before making any
changes::

    pip install pre-commit
    cd bluemvmt-gsf
    pre-commit install

It is a good idea to update the hooks to the latest version::

    pre-commit autoupdate

Don't forget to tell your contributors to also install and use pre-commit.

.. _pre-commit: https://pre-commit.com/

Note
====

This project has been set up using PyScaffold 4.6. For details and usage
information on PyScaffold see https://pyscaffold.org/.
