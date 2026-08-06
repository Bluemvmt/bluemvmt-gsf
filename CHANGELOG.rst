=========
Changelog
=========

0.6.0
==========

- Add Pydantic support for GSF Processing Parameters records (type 4).
- Rebuild bundled libgsf 3.11 (``x86_64`` / ``aarch64``) with Processing
  Parameters JSON and flatten helpers.

0.5.0
==========

- Ship ``bin/`` tools as installable console scripts (``gsf-to-json``,
  ``gsf-to-csv``, ``gsf-to-csv-flatten``).
- Use Poetry as the sole packaging and dependency workflow.
- Support only Linux ``x86_64`` / ``aarch64`` with bundled libgsf **3.11**.
- Remove libgsf 3.08 / 3.09 / 3.10 binaries and multi-version selection.
- Filter ``desired_record`` in the Python wrapper for reliable record selection.
- Repair and strengthen the pytest suite, including deserialize/serialize coverage.
- Replace PyScaffold placeholder documentation and metadata.
