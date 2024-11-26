from gsfpy3_09 import FileMode, open_gsf
from gsfpy3_09.enums import RecordType

from ..models.gsf_records import GsfRecords


def gsf_read(file_name: str) -> GsfRecords:
    with open_gsf(file_name, mode=FileMode.GSF_READONLY_INDEX) as gsf_file:
        current_record_index = 1
        for record_type in RecordType:
            if record_type > 0:
                dataID, record = gsf_file.read(record_type, current_record_index)
