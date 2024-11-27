from datetime import datetime

from pydantic import BaseModel


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
