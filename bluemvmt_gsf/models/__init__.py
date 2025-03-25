from datetime import datetime
from enum import Enum

from pydantic import BaseModel, field_serializer
from pydantic_core import from_json


class RecordType(Enum):
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


class GsfRecordBase(BaseModel):
    time: datetime
    source_file_name: str
    record_id: int
    record_number: int
    record_type: RecordType
    version: str

    @field_serializer("time", when_used="json")
    def serialize_courses_in_order(self, time: datetime):
        return time.isoformat()


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
    min_location: Geo
    max_location: Geo
    min_depth: float
    max_depth: float


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
    #   beam_flags: str
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


class GsfRecord(GsfRecordBase):
    time: datetime
    location: Geo | None = None
    body: (
        GsfSwathBathySummary | GsfSwathBathyPing | GsfComment | GsfHistory | GsfAttitude
    )


class GsfAllRecords(BaseModel):
    records: list[GsfRecord] = []


def deserialize_record(json_src: str) -> GsfRecord:
    return GsfRecord.model_validate(from_json(json_src))

class GsfEM3RunTime(BaseModel):
    model_number: int
    dg_time: datetime
    ping_number: int
    serial_number: int
    system_status: int
    filter_id: int
    min_depth: float
    max_depth: float
    absorption: float
    pulse_length: float
    transmit_beam_width: float
    receive_beam_width: float
    power_reduction: int
    receive_bandwidth: int
    receive_gain: int
    cross_over_angle: int
    ssv_source: int
    swath_width: int
    beam_spacing: int
    coverage_sector: int
    stabilization: int
    port_swath_width: int
    stbd_swath_width: int
    port_coverage_sector: int
    stbd_coverage_sector: int
    hilo_freq_absorp_ratio: int


class GsfEM3Specific(BaseModel):
    model_number: int
    ping_number: int
    serial_number: int
    surface_velocity: float
    transducer_depth: float
    valid_beams: int
    sample_rate: int
    depth_difference: float
    offset_multiplier: int
    run_time: list[GsfEM3RunTime]


class GsfEMRunTime(BaseModel):
    model_number: int
    dg_time: datetime
    ping_counter: int
    serial_number: int
    operator_station_status: bytes
    processing_unit_status: bytes
    bsp_status: bytes
    head_transceiver_status: bytes
    mode: bytes
    filter_id: bytes
    min_depth: float
    max_depth: float
    absorption: float
    tx_pulse_length: float
    tx_beam_width: float
    tx_power_re_max: float
    rx_beam_width: float
    rx_bandwidth: float
    rx_fixed_gain: float
    tvg_cross_over_angle: float
    ssv_source: int
    max_port_swath_width: int
    beam_spacing: int
    max_port_coverage: int
    stabilization: bytes
    max_stbd_coverage: int
    max_stbd_swath_width: int
    durotong_speed: float
    hi_low_absorption_ratio: float
    tx_along_tilt: float
    filter_id_2: int


class GsfEMPUStatus(BaseModel):
    pu_cpu_load: float
    sensor_status: int
    achieved_port_coverage: int
    achieved_stbd_coverage: int
    yaw_stabilization: float


class GsfEM3RawTxSector(BaseModel):
    tilt_angle: float
    focus_range: float
    signal_length: float
    transmit_delay: float
    center_frequency: float
    waveform_id: int
    sector_number: int
    signal_bandwidth: float


class GsfEM3RawSpecific(BaseModel):
    model_number: int
    ping_counter: int
    serial_number: int
    surface_velocity: float
    transducer_depth: float
    valid_detections: int
    sampling_frequency: float
    vehicle_depth: float
    depth_difference: float
    offset_multiplier: int
    transmit_sectors: int
    sector: list[GsfEM3RawTxSector]
    run_time: GsfEMRunTime
    pu_status: GsfEMPUStatus


class GsfEM4TxSector(BaseModel):
    tilt_angle: float
    focus_range: float
    signal_length: float
    transmit_delay: float
    center_frequency: float
    mean_absorption: float
    waveform_id: int
    sector_number: int
    signal_bandwidth: float


class GsfEM4Specific(BaseModel):
    model_number: int
    ping_counter: int
    serial_number: int
    surface_velocity: float
    transducer_depth: float
    valid_detections: int
    sampling_frequency: float
    doppler_corr_scale: int
    vehicle_depth: float
    transmit_sectors: int
    sector: list[GsfEM4TxSector]
    run_time: GsfEMRunTime
    pu_status: GsfEMPUStatus
