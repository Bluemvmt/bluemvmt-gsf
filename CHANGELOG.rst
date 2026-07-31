=========
Changelog
=========

Unreleased
==========

- Use Poetry as the sole packaging and dependency workflow.
- Support only Linux ``x86_64`` / ``aarch64`` with bundled libgsf **3.11**.
- Remove libgsf 3.08 / 3.09 / 3.10 binaries and multi-version selection.
- Filter ``desired_record`` in the Python wrapper for reliable record selection.
- Repair and strengthen the pytest suite, including deserialize/serialize coverage.
- Replace PyScaffold placeholder documentation and metadata.
