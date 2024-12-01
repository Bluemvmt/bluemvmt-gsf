from bluemvmt_gsf.models import GsfRecord, deserialize_record


def test_swath_bathymetric_ping(swath_bathymetric_ping_json):
    record: GsfRecord = deserialize_record(swath_bathymetric_ping_json)
    assert record is not None
