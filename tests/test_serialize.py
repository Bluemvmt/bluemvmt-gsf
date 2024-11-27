from bluemvmt_gsf.reader.gsf3_09 import gsf_read


def test_read(gsf_file, gsf_file_name):
    for _ in gsf_read(gsf_file, gsf_file_name):
        pass
