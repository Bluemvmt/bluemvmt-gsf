from enum import StrEnum

ERRORS = {
    0: "Normal completion",
    -1: "Error opening file",
    -2: "Unrecognized file type",
    -3: "Bad access mode",
    -4: "Read error",
    -5: "Write error",
    -6: "Insufficient size",
    -7: "Record size error",
    -8: "Checksum failure",
    -9: "File close error",
    -10: "Too many array subrecords",
    -11: "Too many open files",
    -12: "Memory allocation failed",
    -13: "Unrecognized record ID",
    -14: "Stream decode failure",
    -15: "Bad seek option",
    -16: "File seek error",
    -17: "Unrecognized sensor ID",
    -18: "Unrecognized data record",
    -19: "Unrecognized array subrecord ID",
    -20: "Unrecognized subrecord ID",
    -21: "Illegal scale factor multiplier",
    -22: "Cannot represent precision",
    -23: "Read to end of file",
    -24: "Bad file handle",
    -25: "Header record decode failed",
    -26: "MB ping record decode failed",
    -27: "SVP record decode failed",
    -28: "Process param record decode failed",
    -35: "File tell error",
    -36: "Index file open error",
    -37: "Corrupt index file error",
    -38: "Scale index calloc error",
    -39: "Record type not available",
    -40: "Summary record decode failed",
    -41: "Summary record encode failed",
    -42: "Invalid number of beams",
    -43: "Invalid record number",
    -44: "Index file read error",
    -45: "Parameter size fixed",
}

SUBRECORDS = {
    0: "Unknown",
    1: "Depth array",
    2: "Across track array",
    3: "Along track array",
    4: "Travel time array",
    5: "Beam angle array",
    6: "Mean calibrated amplitude array",
    7: "Mean relative amplitude array",
    8: "Echo width array",
    9: "Quality factor array",
    10: "Receive heave array",
    11: "Depth error array (obsolete)",
    12: "Across track error array (obsolete)",
    13: "Along track error array (obsolete)",
    14: "Nominal depth array",
    15: "Quality flags array",
    16: "Beam flags array",
    17: "Signal to noise array",
    18: "Beam angle forward array",
    19: "Vertical error array",
    20: "Horizontal error array",
    21: "Intensity series array",
    22: "Sector number array",
    23: "Detection info array",
    24: "Incident beam adjustment array",
    25: "System cleaning array",
    26: "Doppler correction array",
    27: "Sonar vertical uncertainty array",
    28: "Sonar horizontal uncertainty array",
}

RECORD_TYPES = {
    1: "Header record",
    2: "Swath bathymetry ping record",
    3: "Sound velocity profile record",
    4: "Processing parameters record",
    5: "Sensor parameters record",
    6: "Comment record",
    7: "History record",
    8: "Navigation error record (obsolete)",
    9: "Swath bathymetry summary record",
    10: "Single beam ping record",
    11: "Horizontal/Vertical navigation error record",
    12: "Attitude record",
}


class SensorTypes(StrEnum):
    GSF_SWATH_BATHY_SUBRECORD_EM1002_RAW_SPECIFIC = "Kongsberg EM 1002"
    GSF_SWATH_BATHY_SUBRECORD_EM2000_RAW_SPECIFIC = "Kongsberg EM 2000"
    GSF_SWATH_BATHY_SUBRECORD_EM3000_RAW_SPECIFIC = "Kongsberg EM 3000"
    GSF_SWATH_BATHY_SUBRECORD_EM120_RAW_SPECIFIC = "Kongsberg EM 120"
    GSF_SWATH_BATHY_SUBRECORD_EM3002_RAW_SPECIFIC = "Kongsberg EM 3002"
    GSF_SWATH_BATHY_SUBRECORD_EM3000D_RAW_SPECIFIC = "Kongsberg EM 3000"
    GSF_SWATH_BATHY_SUBRECORD_EM3002D_RAW_SPECIFIC = "Kongsberg EM 3002"
    GSF_SWATH_BATHY_SUBRECORD_EM121A_SIS_RAW_SPECIFIC = "Kongsberg EM 121A"
    GSF_SWATH_BATHY_SUBRECORD_EM2040_SPECIFIC = "Kongsberg EM 2040"
    GSF_SWATH_BATHY_SUBRECORD_DELTA_T_SPECIFIC = "Imagenex Detla T"
    GSF_SWATH_BATHY_SUBRECORD_R2SONIC_2022_SPECIFIC = "R2Sonic model 2022"
    GSF_SWATH_BATHY_SUBRECORD_R2SONIC_2024_SPECIFIC = "R2Sonic model 2024"
    GSF_SWATH_BATHY_SUBRECORD_R2SONIC_2020_SPECIFIC = "R2Sonic model 2020"
    GSF_SWATH_BATHY_SUBRECORD_RESON_TSERIES_SPECIFIC = "Reson T Series"
    GSF_SWATH_BATHY_SUBRECORD_KMALL_SPECIFIC = "Kongsberg"


SENSOR_TYPES = {
    141: SensorTypes.GSF_SWATH_BATHY_SUBRECORD_EM1002_RAW_SPECIFIC,
    142: SensorTypes.GSF_SWATH_BATHY_SUBRECORD_EM2000_RAW_SPECIFIC,
    143: SensorTypes.GSF_SWATH_BATHY_SUBRECORD_EM3000_RAW_SPECIFIC,
    144: SensorTypes.GSF_SWATH_BATHY_SUBRECORD_EM120_RAW_SPECIFIC,
    145: SensorTypes.GSF_SWATH_BATHY_SUBRECORD_EM3002_RAW_SPECIFIC,
    146: SensorTypes.GSF_SWATH_BATHY_SUBRECORD_EM3000D_RAW_SPECIFIC,
    147: SensorTypes.GSF_SWATH_BATHY_SUBRECORD_EM3002D_RAW_SPECIFIC,
    148: SensorTypes.GSF_SWATH_BATHY_SUBRECORD_EM121A_SIS_RAW_SPECIFIC,
    149: SensorTypes.GSF_SWATH_BATHY_SUBRECORD_EM2040_SPECIFIC,
    150: SensorTypes.GSF_SWATH_BATHY_SUBRECORD_DELTA_T_SPECIFIC,
    151: SensorTypes.GSF_SWATH_BATHY_SUBRECORD_R2SONIC_2022_SPECIFIC,
    152: SensorTypes.GSF_SWATH_BATHY_SUBRECORD_R2SONIC_2024_SPECIFIC,
    153: SensorTypes.GSF_SWATH_BATHY_SUBRECORD_R2SONIC_2020_SPECIFIC,
    154: SensorTypes.GSF_SWATH_BATHY_SUBRECORD_RESON_TSERIES_SPECIFIC,
    155: SensorTypes.GSF_SWATH_BATHY_SUBRECORD_KMALL_SPECIFIC,
}
