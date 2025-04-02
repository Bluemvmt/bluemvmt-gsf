import os

# This has to come before the import of libgsf after it
os.environ["GSF_VERSION"] = "03.09"

from bluemvmt_gsf.libgsf import GsfFile, open_gsf

def test_to_json(gsf_test_file_path):
    gsf_file: GsfFile = open_gsf(gsf_test_file_path)
    for record in gsf_file.next_json_record():
        print(f"record = {record}")
