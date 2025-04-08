from datetime import datetime
from enum import IntEnum

from pydantic import BaseModel, field_serializer
from pydantic_core import from_json


class RecordType(IntEnum):
    GSF_NEXT_RECORD = 0
    GSF_RECORD_HEADER = 1
    GSF_RECORD_SWATH_BATHYMETRY_PING = 2
    GSF_RECORD_SOUND_VELOCITY_PROFILE = 3
    GSF_RECORD_PROCESSING_PARAMETERS = 4
    GSF_RECORD_SENSOR_PARAMETERS = 5
    GSF_RECORD_COMMENT = 6
    GSF_RECORD_HISTORY = 7
    GSF_RECORD_SWATH_BATHY_SUMMARY = 9
    GSF_RECORD_SINGLE_BEAM_PING = 10
    GSF_RECORD_HV_NAVIGATION_ERROR = 11
    GSF_RECORD_ATTITUDE = 12


class Geo(BaseModel):
    latitude: float
    longitude: float


class GsfAttitude(BaseModel):
    num_measurements: int
    pitch: float | None = None
    roll: float | None = None
    heave: float | None = None
    heading: float | None = None


class GsfHistory(BaseModel):
    host_name: str
    operator_name: str
    command_line: str
    comment: str


class GsfComment(BaseModel):
    comment_length: int
    comment: str


class GsfSwathBathySummary(BaseModel):
    start_time: datetime
    end_time: datetime
    min_latitude: float
    min_longitude: float
    max_latitude: float
    max_longitude: float
    min_depth: float
    max_depth: float

    @property
    def min_location(self) -> Geo:
        return Geo(latitude=self.min_latitude, longitude=self.min_longitude)
    

class GsfHeader(BaseModel):
    version: str


class GsfSensorData(BaseModel):
    ping_counter: int | None = None
    model_number: int | None = None


class GsfSwathBathyPing(BaseModel):
    height: float
    sep: float
    number_beams: int
    center_beam: int
    ping_flags: int | None = None
    reserved: int
    tide_corrector: float
    gps_tide_corrector: float
    depth_corrector: float
    heading: float
    pitch: float
    roll: float
    heave: float
    course: float
    speed: float
    depth: list[float] | None = None
    nominal_depth: list[float] | None = None
    across_track: list[float] | None = None
    along_track: list[float] | None = None
    travel_time: list[float] | None = None
    beam_angle: list[float] | None = None
    mc_amplitude: list[float] | None = None
    mr_amplitude: list[float] | None = None
    echo_width: list[float] | None = None
    quality_factor: list[float] | None = None
    receive_heave: list[float] | None = None
    depth_error: list[float] | None = None
    across_track_error: list[float] | None = None
    along_track_error: list[float] | None = None
    quality_flags: str | None = None
    beam_flags: list[int] | None = None
    signal_to_noise: float | None = None
    beam_angle_forward: list[float] | None = None
    vertical_error: list[float] | None = None
    horizontal_error: list[float] | None = None
    sector_number: list[int] | None = None
    detection_info: list[int] | None = None
    incident_beam_adj: list[float] | None = None
    system_cleaning: list[int] | None = None
    doppler_corr: list[float] | None = None
    sonar_vert_uncert: list[float] | None = None
    sonar_horiz_uncert: list[float] | None = None
    detection_window: list[float] | None = None
    mean_abs_coeff: list[float] | None = None
    sensor_id: int
    sensor_data: GsfSensorData | None = None


class GsfRecord(BaseModel):
    record_type: RecordType
    mb_ping: GsfSwathBathyPing | None = None
    summary: GsfSwathBathySummary | None = None
    header: GsfHeader | None = None


class GsfAllRecords(BaseModel):
    records: list[GsfRecord] = []


def deserialize_record(json_src: str) -> GsfRecord:
    return GsfRecord.model_validate(from_json(json_src))
