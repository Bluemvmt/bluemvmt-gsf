import logging

from gsfpy3_09 import GsfFile

from ..models import GsfAttitude, GsfRecord, RecordType
from . import timespec_to_datetime

_log = logging.getLogger("bluemvmt_gsf.reader")


def gsf_read(gsf_file: GsfFile, file_name: str) -> GsfRecord:
    num_records = gsf_file.get_number_records(
        desired_record=RecordType.GSF_RECORD_HEADER.value
    )
    _log.debug(f"Reading {num_records} GSF_RECORD_HEADER records")
    for index in range(1, num_records):
        data_id, record = gsf_file.read(RecordType.GSF_RECORD_HEADER.value, index)
        _log.debug(f"data_id={data_id}, record={record}")

    num_records = gsf_file.get_number_records(
        desired_record=RecordType.GSF_RECORD_ATTITUDE.value
    )
    _log.debug(f"Reading {num_records} GSF_RECORD_ATTITUDE records")
    for index in range(1, num_records):
        data_id, record = gsf_file.read(RecordType.GSF_RECORD_ATTITUDE.value, index)
        gsf_attitude = GsfAttitude(
            num_measurements=float(record.attitude.num_measurements),
            pitch=float(record.attitude.pitch.contents.value),
            roll=float(record.attitude.roll.contents.value),
            heave=float(record.attitude.heave.contents.value),
            heading=float(record.attitude.heading.contents.value),
        )
        pydantic_record = GsfRecord(
            source_file_name=file_name,
            record_id=data_id.recordID,
            record_number=data_id.record_number,
            version="03_09",
            record_type=RecordType.GSF_RECORD_ATTITUDE,
            time=timespec_to_datetime(record.attitude.attitude_time.contents),
            attitude=gsf_attitude,
        )
        yield pydantic_record
