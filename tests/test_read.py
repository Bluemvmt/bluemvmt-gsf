from bluemvmt_gsf.reader.gsf3_09 import gsf_read


def test_read(gsf_file, gsf_file_name):
    for record in gsf_read(gsf_file, gsf_file_name):
        print(f"record={record.model_dump_json()}")
