from pathlib import Path
from platform import machine

import pytest

from bluemvmt_gsf.libgsf import GsfException, GsfFile
from bluemvmt_gsf.libgsf.bindings import Gsf, GsfVersion, SUPPORTED_ARCHITECTURES
from bluemvmt_gsf.models import (
    GsfComment,
    GsfSwathBathyPing,
    GsfSwathBathySummary,
    RecordType,
    deserialize_flattened_record,
    deserialize_record,
)


def test_to_json(gsf_test_file_path):
    with GsfFile(path=gsf_test_file_path) as gsf_file:
        records = list(gsf_file.next_json_record())

    assert len(records) == 5
    for raw in records:
        model = deserialize_record(raw)
        assert model.record_type in RecordType


def test_to_json_with_denormalized_fields(gsf_test_file_path):
    with GsfFile(
        path=gsf_test_file_path, include_denormalized_fields=True
    ) as gsf_file:
        records = [deserialize_record(raw) for raw in gsf_file.next_json_record()]

    assert len(records) == 5
    ping = next(
        r
        for r in records
        if r.record_type == RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING
    )
    assert ping.file_name == Path(gsf_test_file_path).name
    assert ping.timestamp is not None
    assert ping.latitude is not None
    assert ping.longitude is not None
    assert isinstance(ping.json_record, GsfSwathBathyPing)


def test_to_json_flattened(gsf_test_file_path):
    with GsfFile(path=gsf_test_file_path, flatten=True) as gsf_file:
        records = [
            deserialize_flattened_record(raw) for raw in gsf_file.next_json_record()
        ]

    assert len(records) == 5
    ping = next(
        r
        for r in records
        if r.record_type == RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING
    )
    assert ping.mb_number_beams == 7
    assert ping.sensor_name


def test_to_pydantic_record_types(gsf_test_file_path):
    with GsfFile(path=gsf_test_file_path) as gsf_file:
        records = [deserialize_record(raw) for raw in gsf_file.next_json_record()]

    types = {record.record_type for record in records}
    assert RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING in types
    assert RecordType.GSF_RECORD_SWATH_BATHY_SUMMARY in types

    for record in records:
        if record.record_type == RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING:
            assert isinstance(record.json_record, GsfSwathBathyPing)
        elif record.record_type == RecordType.GSF_RECORD_SWATH_BATHY_SUMMARY:
            assert isinstance(record.json_record, GsfSwathBathySummary)
        elif record.record_type == RecordType.GSF_RECORD_COMMENT:
            assert isinstance(record.json_record, GsfComment)


def test_get_num_records_swath_bathy_ping(gsf_test_file_path):
    with GsfFile(path=gsf_test_file_path) as gsf_file:
        assert (
            gsf_file.get_number_records(
                desired_record=RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING
            )
            == 3
        )


def test_get_num_records_summary(gsf_test_file_path):
    with GsfFile(path=gsf_test_file_path) as gsf_file:
        assert (
            gsf_file.get_number_records(
                desired_record=RecordType.GSF_RECORD_SWATH_BATHY_SUMMARY
            )
            == 1
        )


def test_get_swath_bathy_ping(gsf_test_file_path):
    with GsfFile(path=gsf_test_file_path) as gsf_file:
        recs = [
            deserialize_record(raw)
            for raw in gsf_file.next_json_record(
                desired_record=RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING
            )
        ]

    assert len(recs) == 3
    assert all(
        r.record_type == RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING for r in recs
    )
    assert all(isinstance(r.json_record, GsfSwathBathyPing) for r in recs)


def test_missing_file_raises():
    with pytest.raises(GsfException):
        GsfFile(path="/tmp/does-not-exist-bluemvmt-gsf.gsf")


def test_default_version_is_311():
    assert GsfVersion._3_11 == "03.11"
    assert list(GsfVersion) == [GsfVersion._3_11]


def test_bundled_libraries_present():
    lib_dir = Path(__file__).resolve().parents[2] / "src/bluemvmt_gsf/libgsf/lib"
    for arch in SUPPORTED_ARCHITECTURES:
        path = lib_dir / f"libgsf-{arch}-03.11.so"
        assert path.is_file(), f"missing bundled library: {path}"
        assert path.stat().st_size > 0


def test_load_default_library():
    gsf = Gsf()
    assert Path(gsf._libgsf_abs_path).name == f"libgsf-{machine()}-03.11.so"
