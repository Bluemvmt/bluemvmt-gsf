============
bluemvmt-gsf
============

``bluemvmt-gsf`` decodes Generic Sensor Format (GSF) files into Pydantic models
using a bundled Linux ``libgsf`` 3.11 shared library.

Supported platforms:

- Linux ``x86_64``
- Linux ``aarch64``
- Python 3.11+

Quick start::

    from bluemvmt_gsf.libgsf import GsfFile
    from bluemvmt_gsf.models import deserialize_record

    with GsfFile("survey.gsf", include_denormalized_fields=True) as gsf:
        for raw in gsf.next_json_record():
            print(deserialize_record(raw))


Contents
========

.. toctree::
   :maxdepth: 2

   Overview <readme>
   Contributions & Help <contributing>
   License <license>
   Authors <authors>
   Changelog <changelog>
   Module Reference <api/modules>


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
