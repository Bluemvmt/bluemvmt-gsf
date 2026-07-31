from bluemvmt_gsf.models import GsfSwathBathyPing, RecordType, deserialize_record


def test_swath_bathymetric_ping(swath_bathymetric_ping_json):
    record = deserialize_record(swath_bathymetric_ping_json)

    assert record.record_type == RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING
    assert isinstance(record.json_record, GsfSwathBathyPing)
    assert record.json_record.number_beams == 7
    assert record.json_record.sensor_name
    assert record.file_name == "GSF3_09_test_file.gsf"
    assert record.timestamp is not None
    assert record.latitude is not None
    assert record.longitude is not None
