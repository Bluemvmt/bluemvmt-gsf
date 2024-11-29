from bluemvmt_gsf.models import GsfAllRecords
from bluemvmt_gsf.reader.gsf3_09 import gsf_read


def test_read(gsf_file, gsf_file_name, save_json):
    gsf_records = GsfAllRecords()
    for record in gsf_read(gsf_file, gsf_file_name):
        gsf_records.records.append(record)

    if save_json:
        with open(f"{gsf_file_name}.json", mode="w") as f:
            f.write(gsf_records.model_dump_json())
