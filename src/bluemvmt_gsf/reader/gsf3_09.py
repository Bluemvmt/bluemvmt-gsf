import ctypes
import logging

from gsfpy3_09 import GsfFile
from gsfpy3_09.gsfSensorSpecific import c_gsfEM3Specific
from gsfpy3_09.gsfSwathBathyPing import c_gsfSwathBathyPing

from ..models import (
    Geo,
    GsfAttitude,
    GsfComment,
    GsfEM3Specific,
    GsfHistory,
    GsfRecord,
    GsfSwathBathyPing,
    GsfSwathBathySummary,
    RecordType,
)
from . import timespec_to_datetime

_log = logging.getLogger("bluemvmt_gsf.reader")


def _char_pointer_to_str(original):
    c_string = ctypes.cast(original, ctypes.c_char_p)
    return c_string.value.decode("utf-8")


def _ubyte_pointer_to_str(original) -> str | None:
    try:
        return original.contents.value.decode("utf-8")
    except ValueError:
        return None


def _double_pointer_to_array(original, num_values) -> list[float] | None:
    try:
        float_list: list[float] = original[0:num_values]
        return float_list
    except SystemError:
        return None


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
            comment=_char_pointer_to_str(record.comment.comment),
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

    num_records = gsf_file.get_number_records(
        desired_record=RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING.value
    )
    _log.debug(f"Reading {num_records} GSF_RECORD_SWATH_BATHYMETRY_PING records")
    for index in range(1, num_records + 1):
        data_id, record = gsf_file.read(
            RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING.value, index
        )
        gsf_ping = _convert_swath_bathy_ping(record.mb_ping)
        pydantic_record = GsfRecord(
            source_file_name=file_name,
            record_id=data_id.recordID,
            record_number=data_id.record_number,
            version="03_09",
            record_type=RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING,
            time=timespec_to_datetime(record.mb_ping.ping_time),
            mb_ping=gsf_ping,
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


def _convert_em3_specific(sensor: c_gsfEM3Specific) -> GsfEM3Specific | None:
    _log.debug(f"sensor = {sensor}")
    return None


def _convert_swath_bathy_ping(ping: c_gsfSwathBathyPing) -> GsfSwathBathyPing:
    number_beams: int = ping.number_beams
    #    _log.debug(f"sensor_data = {ping.sensor_data.gsfEM3Specific.model_number}")
    return GsfSwathBathyPing(
        height=ping.height,
        sep=ping.sep,
        number_beams=ping.number_beams,
        center_beam=ping.center_beam,
        ping_flags_bits=ping.ping_flags,
        reserved=ping.reserved,
        tide_corrector=ping.tide_corrector,
        gps_tide_corrector=ping.gps_tide_corrector,
        depth_corrector=ping.depth_corrector,
        heading=ping.heading,
        pitch=ping.pitch,
        roll=ping.roll,
        heave=ping.heave,
        course=ping.course,
        speed=ping.speed,
        sensor_id=ping.sensor_id,
        quality_flags=_ubyte_pointer_to_str(ping.quality_flags),
        depth=_double_pointer_to_array(ping.depth, number_beams),
        nominal_depth=_double_pointer_to_array(ping.nominal_depth, number_beams),
        across_track=_double_pointer_to_array(ping.across_track, number_beams),
        along_track=_double_pointer_to_array(ping.along_track, number_beams),
        travel_time=_double_pointer_to_array(ping.travel_time, number_beams),
        beam_angle=_double_pointer_to_array(ping.beam_angle, number_beams),
        mc_amplitude=_double_pointer_to_array(ping.mc_amplitude, number_beams),
        mr_amplitude=_double_pointer_to_array(ping.mr_amplitude, number_beams),
        echo_width=_double_pointer_to_array(ping.echo_width, number_beams),
        quality_factor=_double_pointer_to_array(ping.quality_factor, ping.number_beams),
        receive_heave=_double_pointer_to_array(ping.receive_heave, ping.number_beams),
        depth_error=_double_pointer_to_array(ping.depth_error, ping.number_beams),
        across_track_error=_double_pointer_to_array(
            ping.across_track_error, ping.number_beams
        ),
        along_track_error=_double_pointer_to_array(
            ping.along_track_error, ping.number_beams
        ),
    )
