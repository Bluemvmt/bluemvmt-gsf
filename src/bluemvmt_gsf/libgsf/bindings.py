from ctypes import CDLL, POINTER, c_char_p, c_int, c_ubyte, c_uint32
from os import environ
from pathlib import Path
from platform import machine

from ..models import RecordType

gsf_version = "03.09"
_libgsf_abs_path = str(Path(__file__).parent / "lib" / f"libgsf-{machine()}-{gsf_version}.so")

# Check if the libgsf shared object library location is specified in the environment.
# If so, use the specified library in preference to the bundled version. Handle the
# case where the library cannot be found.
if "GSFPY3_08_LIBGSF_PATH" in environ:
    _libgsf_abs_path = environ["GSFPY3_08_LIBGSF_PATH"]

try:
    _libgsf = CDLL(_libgsf_abs_path)
except OSError as osex:
    raise Exception(
        f"Cannot load shared library from {_libgsf_abs_path}. Set the "
        f"$GSFPY3_08_LIBGSF_PATH environment variable to the correct path, "
        f"or remove it from the environment to use the default version."
    ) from osex


_libgsf.gsfClose.argtypes = [c_int]
_libgsf.gsfClose.restype = c_int

_libgsf.gsfOpen.argtypes = [c_char_p, c_int, (POINTER(c_int))]
_libgsf.gsfOpen.restype = c_int

_libgsf.gsfOpenBuffered.argtypes = [c_char_p, c_int, (POINTER(c_int)), c_int]
_libgsf.gsfOpenBuffered.restype = c_int

_libgsf.gsfIntError.argtypes = []
_libgsf.gsfIntError.restype = c_int

_libgsf.gsfStringError.argtypes = []
_libgsf.gsfStringError.restype = c_char_p


_libgsf.gsfRead.argtypes = [
    c_int,
    c_int,
    c_uint32,
    c_uint32,
    POINTER(c_ubyte),
    c_int,
]
_libgsf.gsfRead.restype = c_int

_libgsf.gsfSeek.argtypes = [c_int, c_int]
_libgsf.gsfSeek.restype = c_int

_libgsf.gsfRecord_toJson.argtypes = [c_uint32, c_uint32]
_libgsf.gsfRecord_toJson.restype = c_char_p

_libgsf.gsfGetNumberRecords.argtypes = [c_int, c_int]
_libgsf.gsfGetNumberRecords.restype = c_int

from ctypes import Structure, c_int, c_uint


class c_gsfNextJsonRecord(Structure):
    _fields_ = [
        ("last_return_value", c_int),
        ("json_record", c_char_p)
    ]

_libgsf.gsfNextJsonRecord.argtypes = [c_int, c_int]
_libgsf.gsfNextJsonRecord.restype = c_gsfNextJsonRecord

def gsfOpen(filename: bytes, p_handle) -> int:
    """
    :param filename: bytestring e.g. b'path/to/file.gsf'
    :param mode: gsfpy3_08.enums.FileMode
    :param p_handle: Instance of POINTER(c_int)
    :return: 0 if successful, otherwise -1
    """
    return _libgsf.gsfOpen(filename, 2, p_handle)


def gsfOpenBuffered(filename: bytes, p_handle, buf_size: int) -> int:
    """
    :param filename: bytestring e.g. b'path/to/file.gsf'
    :param mode: gsfpy3_08.enums.FileMode
    :param p_handle: Instance of POINTER(c_int)
    :param buf_size: c_int
    :return: 0 if successful, otherwise -1
    """
    return _libgsf.gsfOpenBuffered(filename, 2, p_handle, buf_size)


def gsfNextJsonRecord(handle: c_int, desired_record: c_int) -> c_gsfNextJsonRecord:
    return _libgsf.gsfNextJsonRecord(handle, desired_record)


def gsfClose(handle: c_int) -> int:
    """
    :param handle: c_int
    :return: 0 if successful, otherwise -1
    """
    return _libgsf.gsfClose(handle)


def gsfRead(
    handle: c_int,
    desired_record: RecordType,
    p_data_id,
    p_records,
    p_stream=None,
    max_size=0,
) -> int:
    """
    :param handle: int
    :param desired_record: gsfpy3_08.enums.RecordType
    :param p_data_id: POINTER(gsfpy3_08.gsfDataID.c_gsfDataID)
    :param p_records: POINTER(gsfpy3_08.gsfRecords.c_gsfRecords)
    :param p_stream: POINTER(c_ubyte)
    :param max_size: int
    :return: number of bytes read if successful, otherwise -1. Note that contents of the
             POINTER parameters p_data_id, p_records and p_stream will be updated upon
             successful read.
    """
    return _libgsf.gsfRead(
        handle,
        desired_record,
        p_data_id,
        p_records,
        p_stream,
        max_size,
    )

def gsfGetNumberRecords(handle: c_int, desired_record: RecordType) -> int:
    """
    File must be open for direct access (GSF_READONLY_INDEX or GSF_UPDATE_INDEX)
    :param handle: c_int
    :param desired_record: gsfpy3_08.enums.RecordType
    :return: number of records of type desired_record, otherwise -1
    """
    return _libgsf.gsfGetNumberRecords(handle, desired_record)


def gsfRecordToJson(p_data_id: c_uint32, p_records: c_uint32) -> c_char_p:
    return _libgsf.gsfRecord_toJson(p_data_id, p_records)


def gsfIntError() -> int:
    """
    :return: The last value that the GSF error code was set to (c_int).
    """
    return _libgsf.gsfIntError()


def gsfStringError() -> bytes:
    """
    :return: The last value that the GSF error message was set to (c_char_p).
    """
    return _libgsf.gsfStringError()
