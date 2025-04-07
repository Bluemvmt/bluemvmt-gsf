from bluemvmt_gsf import gsf

gsf.version = "03.10"

from bluemvmt_gsf.libgsf import GsfFile, open_gsf
from bluemvmt_gsf.models import deserialize_record, GsfRecord, RecordType

def test_to_json(gsf_test_file_path):
    gsf_file: GsfFile = open_gsf(gsf_test_file_path)
    try:
        count: int = 0
        for record in gsf_file.next_json_record():
            if record is not None:
                print(f"rec = {record.decode()}")
            count += 1
        assert(count == 5)
    finally:
        gsf_file.close()


def test_to_pydantic(gsf_test_file_path):
    gsf_file: GsfFile = open_gsf(gsf_test_file_path)
    try:
        for record in gsf_file.next_json_record(desired_record=0):
            if record != None:
                deserialize_record(record)
    finally:
        gsf_file.close()
    
    gsf_file: GsfFile = open_gsf(gsf_test_file_path)
    try:
        for record in gsf_file.next_json_record(desired_record=0):
            if record != None:
                deserialize_record(record)
    finally:
        gsf_file.close()


def test_get_num_records_swath_bathy_ping(gsf_test_file_path):
    gsf_file: GsfFile = open_gsf(gsf_test_file_path)
    num_recs = gsf_file.get_number_records(desired_record=RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING)
    gsf_file.close()
    assert(num_recs == 3)


def test_get_num_records_summary(gsf_test_file_path):
    gsf_file: GsfFile = open_gsf(gsf_test_file_path)
    num_recs = gsf_file.get_number_records(desired_record=RecordType.GSF_RECORD_SWATH_BATHY_SUMMARY)
    gsf_file.close()
    assert(num_recs == 1)


def test_get_swath_bathy_ping(gsf_test_file_path):
    gsf_file: GsfFile = open_gsf(gsf_test_file_path)
    recs: list[GsfRecord] = []

    count: int = 0
    for record in gsf_file.next_json_record(desired_record=RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING):
        if record != None:
            print(f"rec = {record.decode()[0:60]}")
            recs.append(record)
        count += 1
        if count > 10:
            break

    assert(len(recs) == 3)

# def test_get_summary(gsf_test_file_path):
#     gsf_file: GsfFile = open_gsf(gsf_test_file_path)
#     recs: list[GsfRecord] = []

#     for record in gsf_file.next_json_record(desired_record=RecordType.GSF_RECORD_SWATH_BATHY_SUMMARY):
#         if record != None:
#             recs.append(record)

#     assert(len(recs) == 1)