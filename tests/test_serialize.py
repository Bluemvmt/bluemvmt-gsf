import json

from bluemvmt_gsf.libgsf import GsfFile
from bluemvmt_gsf.models import deserialize_record


def test_round_trip_serialize(gsf_test_file_path):
    with GsfFile(path=gsf_test_file_path) as gsf_file:
        records = list(gsf_file.next_json_record())

    assert len(records) == 5

    for raw in records:
        model = deserialize_record(raw)
        dumped = json.loads(model.model_dump_json())
        assert dumped["record_type"] == model.record_type
        reloaded = deserialize_record(json.dumps(dumped))
        assert reloaded.record_type == model.record_type
