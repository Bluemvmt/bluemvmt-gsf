from ctypes import CDLL, POINTER, Structure, c_char_p, c_int, c_ubyte, c_uint32
from enum import StrEnum
from pathlib import Path
from platform import machine

from ..models import RecordType


class GsfVersion(StrEnum):
    _3_08 = "03.08"
    _3_09 = "03.09"
    _3_10 = "03.10"


class c_gsfNextJsonRecord(Structure):
    _fields_ = [("last_return_value", c_int), ("json_record", c_char_p)]


class Gsf:
    def __init__(self, gsf_version: GsfVersion = GsfVersion._3_10):
        try:
            self._libgsf_abs_path = str(
                Path(__file__).parent
                / "lib"
                / f"libgsf-{machine()}-{gsf_version.value}.so"
            )
            self._libgsf = CDLL(self._libgsf_abs_path)
        except OSError as osex:
            raise Exception(
                f"Cannot load shared library from {self._libgsf_abs_path}. Set the "
                f"$GSFPY3_08_LIBGSF_PATH environment variable to the correct path, "
                f"or remove it from the environment to use the default version."
            ) from osex

        self._libgsf.gsfClose.argtypes = [c_int]
        self._libgsf.gsfClose.restype = c_int

        self._libgsf.gsfOpen.argtypes = [c_char_p, c_int, (POINTER(c_int))]
        self._libgsf.gsfOpen.restype = c_int

        self._libgsf.gsfOpenBuffered.argtypes = [
            c_char_p,
            c_int,
            (POINTER(c_int)),
            c_int,
        ]
        self._libgsf.gsfOpenBuffered.restype = c_int

        self._libgsf.gsfIntError.argtypes = []
        self._libgsf.gsfIntError.restype = c_int

        self._libgsf.gsfStringError.argtypes = []
        self._libgsf.gsfStringError.restype = c_char_p

        self._libgsf.gsfRead.argtypes = [
            c_int,
            c_int,
            c_uint32,
            c_uint32,
            POINTER(c_ubyte),
            c_int,
        ]
        self._libgsf.gsfRead.restype = c_int

        self._libgsf.gsfSeek.argtypes = [c_int, c_int]
        self._libgsf.gsfSeek.restype = c_int

        self._libgsf.gsfGetNumberRecords.argtypes = [c_int, c_int]
        self._libgsf.gsfGetNumberRecords.restype = c_int

        self._libgsf.gsfNextJsonRecord.argtypes = [c_int, c_int]
        self._libgsf.gsfNextJsonRecord.restype = c_gsfNextJsonRecord

    def gsfOpenForJson(
        self,
        filename: bytes,
        mode: int,
        p_handle,
        bufsize: int,
        include_denormalized_fields: int,
        flatten: int,
    ) -> int:
        return self._libgsf.gsfOpenForJson(
            filename, mode, p_handle, bufsize, include_denormalized_fields, flatten
        )

    def gsfOpen(self, filename: bytes, mode: int, p_handle) -> int:
        """
        :param filename: bytestring e.g. b'path/to/file.gsf'
        :param p_handle: Instance of POINTER(c_int)
        :return: 0 if successful, otherwise -1
        """
        return self._libgsf.gsfOpen(filename, mode, p_handle)

    def gsfOpenBuffered(
        self, filename: bytes, mode: int, p_handle, buf_size: int
    ) -> int:
        """
        :param filename: bytestring e.g. b'path/to/file.gsf'
        :param p_handle: Instance of POINTER(c_int)
        :param buf_size: c_int
        :return: 0 if successful, otherwise -1
        """
        return self._libgsf.gsfOpenBuffered(filename, mode, p_handle, buf_size)

    def gsfNextJsonRecord(
        self, handle: c_int, desired_record: c_int
    ) -> c_gsfNextJsonRecord:
        return self._libgsf.gsfNextJsonRecord(handle, desired_record)

    def gsfClose(self, handle: c_int) -> int:
        """
        :param handle: c_int
        :return: 0 if successful, otherwise -1
        """
        return self._libgsf.gsfClose(handle)

    def gsfGetNumberRecords(self, handle: c_int, desired_record: RecordType) -> int:
        """
        File must be open for direct access (GSF_READONLY_INDEX or GSF_UPDATE_INDEX)
        :param handle: c_int
        :param desired_record: gsfpy3_08.enums.RecordType
        :return: number of records of type desired_record, otherwise -1
        """
        return self._libgsf.gsfGetNumberRecords(handle, desired_record)

    def gsfIntError(self) -> int:
        """
        :return: The last value that the GSF error code was set to (c_int).
        """
        return self._libgsf.gsfIntError()

    def gsfStringError(self) -> bytes:
        """
        :return: The last value that the GSF error message was set to (c_char_p).
        """
        return self._libgsf.gsfStringError()
