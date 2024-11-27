import ctypes
import logging

from gsfpy3_09 import GsfFile

from ..models import (
    Geo,
    GsfAttitude,
    GsfComment,
    GsfHistory,
    GsfRecord,
    GsfSwathBathySummary,
    RecordType,
)
from . import timespec_to_datetime

_log = logging.getLogger("bluemvmt_gsf.reader")


def char_pointer_to_str(original):
    c_string = ctypes.cast(original, ctypes.c_char_p)
    return c_string.value.decode("utf-8")


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
    for index in range(1, num_records + 1):
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

    num_records = gsf_file.get_number_records(
        desired_record=RecordType.GSF_RECORD_HISTORY.value
    )
    _log.debug(f"Reading {num_records} GSF_RECORD_HISTORY records")
    for index in range(1, num_records + 1):
        data_id, record = gsf_file.read(RecordType.GSF_RECORD_HISTORY.value, index)
        gsf_history = GsfHistory(
            host_name=record.history.host_name.decode("utf-8"),
            operator_name=record.history.operator_name.decode("utf-8"),
            command_line=record.history.command_line.contents.value.decode("utf-8"),
            comment=record.history.comment.contents.value.decode("utf-8"),
        )
        pydantic_record = GsfRecord(
            source_file_name=file_name,
            record_id=data_id.recordID,
            record_number=data_id.record_number,
            version="03_09",
            record_type=RecordType.GSF_RECORD_HISTORY,
            time=timespec_to_datetime(record.history.history_time),
            history=gsf_history,
        )
        yield pydantic_record

    num_records = gsf_file.get_number_records(
        desired_record=RecordType.GSF_RECORD_COMMENT.value
    )
    _log.debug(f"Reading {num_records} GSF_RECORD_COMMENT records")
    for index in range(1, num_records + 1):
        data_id, record = gsf_file.read(RecordType.GSF_RECORD_COMMENT.value, index)
        comment_length = record.comment.comment_length
        gsf_comment = GsfComment(
            comment_length=comment_length,
            comment=char_pointer_to_str(record.comment.comment),
        )
        pydantic_record = GsfRecord(
            source_file_name=file_name,
            record_id=data_id.recordID,
            record_number=data_id.record_number,
            version="03_09",
            record_type=RecordType.GSF_RECORD_COMMENT,
            time=timespec_to_datetime(record.comment.comment_time),
            comment=gsf_comment,
        )
        yield pydantic_record

    num_records = gsf_file.get_number_records(
        desired_record=RecordType.GSF_RECORD_SWATH_BATHY_SUMMARY.value
    )
    _log.debug(f"Reading {num_records} GSF_RECORD_SWATH_BATHY_SUMMARY records")
    for index in range(1, num_records + 1):
        data_id, record = gsf_file.read(
            RecordType.GSF_RECORD_SWATH_BATHY_SUMMARY.value, index
        )
        gsf_summary = _convert_swath_bathy_summary(record.summary)
        pydantic_record = GsfRecord(
            source_file_name=file_name,
            record_id=data_id.recordID,
            record_number=data_id.record_number,
            version="03_09",
            record_type=RecordType.GSF_RECORD_SWATH_BATHY_SUMMARY,
            time=timespec_to_datetime(record.summary.start_time),
            summary=gsf_summary,
        )
        yield pydantic_record


def _convert_swath_bathy_summary(summary) -> GsfSwathBathySummary:
    return GsfSwathBathySummary(
        start_time=timespec_to_datetime(summary.start_time),
        end_time=timespec_to_datetime(summary.end_time),
        min_location=Geo(
            latitude=summary.min_latitude, longitude=summary.min_longitude
        ),
        max_location=Geo(
            latitude=summary.max_latitude, longitude=summary.max_longitude
        ),
        min_depth=summary.min_depth,
        max_depth=summary.max_depth,
    )
