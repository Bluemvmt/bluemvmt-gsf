.. image:: https://github.com/Bluemvmt/bluemvmt-gsf/actions/workflows/ci.yml/badge.svg
    :alt: Build Status
    :target: https://github.com/Bluemvmt/bluemvmt-gsf/actions/workflows/ci.yml
.. image:: https://img.shields.io/pypi/v/bluemvmt-gsf.svg
    :alt: PyPI
    :target: https://pypi.org/project/bluemvmt-gsf/

============
bluemvmt-gsf
============

Decode Generic Sensor Format (GSF) files into Pydantic models.

``bluemvmt-gsf`` wraps a bundled, JSON-enabled ``libgsf`` **3.11** shared library
with ``ctypes`` and exposes typed Python records that are easier to work with
than a raw C binding.

Platform support
================

- **OS:** Linux only
- **Architectures:** ``x86_64`` and ``aarch64``
- **Python:** 3.11+
- **Native library:** GSF / libgsf **3.11** only
- **glibc:** the bundled binaries require **glibc 2.33+** (for example Ubuntu 22.04+)

Older on-disk GSF files remain readable through libgsf 3.11 compatibility paths.
Windows and macOS native libraries are not provided.

Installation
============

From PyPI::

    pip install bluemvmt-gsf

For local development with Poetry::

    poetry install --with dev,docs

Command-line tools
==================

After installation the following commands are available on ``PATH``:

- ``gsf-to-json`` — time deserialize of records from a binary GSF file
- ``gsf-to-csv`` / ``gsf-to-csv-flatten`` — convert NDJSON record streams to CSV

Example::

    gsf-to-json --gsf-file survey.gsf --num-records 10

From a source checkout you can also run the thin wrappers under ``bin/``
(with the package installed), or ``poetry run gsf-to-json ...``.

Usage
=====

Decode records from a GSF file::

    from bluemvmt_gsf.libgsf import GsfFile
    from bluemvmt_gsf.models import RecordType, deserialize_record

    with GsfFile("survey.gsf", include_denormalized_fields=True) as gsf:
        for raw in gsf.next_json_record():
            record = deserialize_record(raw)
            print(record.record_type, record.timestamp)

Filter to swath bathymetry pings::

    with GsfFile("survey.gsf") as gsf:
        for raw in gsf.next_json_record(
            desired_record=RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING
        ):
            ping = deserialize_record(raw).json_record
            print(ping.number_beams, ping.sensor_name)

Flattened JSON is also supported::

    from bluemvmt_gsf.models import deserialize_flattened_record

    with GsfFile("survey.gsf", flatten=True) as gsf:
        for raw in gsf.next_json_record():
            print(deserialize_flattened_record(raw))

Development
===========

Install pre-commit hooks once::

    poetry run pre-commit install

Run the test suite::

    poetry run pytest

Build documentation::

    poetry run sphinx-build -b html docs docs/_build/html

Build distribution artifacts::

    poetry build

The resulting wheel and sdist include both
``libgsf-x86_64-03.11.so`` and ``libgsf-aarch64-03.11.so``.

License
=======

MIT. See ``LICENSE.txt``.
