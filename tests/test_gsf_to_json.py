from bluemvmt_gsf.libgsf import GsfFile, open_gsf


def test_to_json(gsf_file, gsf_file_name):
    gsf_file: GsfFile = open_gsf(gsf_file)
    for record in gsf_file.read():
        print(f"record = {record}")
