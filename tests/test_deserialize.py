from datetime import datetime, timezone

from bluemvmt_gsf.models import (
    GsfProcessingParameters,
    GsfSwathBathyPing,
    RecordType,
    deserialize_flattened_record,
    deserialize_record,
)


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


def test_processing_parameters(processing_parameters_json):
    record = deserialize_record(processing_parameters_json)

    assert record.record_type == RecordType.GSF_RECORD_PROCESSING_PARAMETERS
    assert isinstance(record.json_record, GsfProcessingParameters)
    assert record.json_record.param_time == datetime.fromtimestamp(
        1541193704.5599995, tz=timezone.utc
    )
    assert record.json_record.number_parameters == 3
    assert record.json_record.parameters == [
        "REFERENCE_TIME=2018-11-02 18:41:44",
        "NUMBER_OF_TRANSMITTERS=1",
        "NUMBER_OF_RECEIVERS=1",
    ]
    assert record.file_name == "GSF3_09_test_file.gsf"
    assert record.timestamp == 1541193704.5599995


def test_processing_parameters_flattened(processing_parameters_flattened_json):
    record = deserialize_flattened_record(processing_parameters_flattened_json)

    assert record.record_type == RecordType.GSF_RECORD_PROCESSING_PARAMETERS
    assert record.number_parameters == 3
    assert record.parameters == [
        "REFERENCE_TIME=2018-11-02 18:41:44",
        "NUMBER_OF_TRANSMITTERS=1",
        "NUMBER_OF_RECEIVERS=1",
    ]
    assert record.timestamp == 1541193704.5599995
    assert record.file_name == "GSF3_09_test_file.gsf"
