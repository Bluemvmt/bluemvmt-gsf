from bluemvmt_gsf.models import GsfRecord
from bluemvmt_gsf.reader.gsf3_09 import gsf_read


def test_read(gsf_file, gsf_file_name, save_json, output_rec):
    with open(f"{gsf_file_name}.json", "w") as f:
        record: GsfRecord
        for record in gsf_read(gsf_file, gsf_file_name):
            if save_json:
                f.write(record.model_dump_json() + "\n")

    print("We have all of the records...")
