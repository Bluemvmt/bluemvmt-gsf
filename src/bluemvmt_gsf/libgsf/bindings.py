import sys
from ctypes import CDLL, POINTER, Structure, c_char_p, c_int, c_ubyte, c_uint32
from enum import StrEnum
from pathlib import Path
from platform import machine, system

from ..models import RecordType

SUPPORTED_ARCHITECTURES = ("x86_64", "aarch64")
GSF_LIBRARY_VERSION = "03.11"


class GsfVersion(StrEnum):
    """Bundled libgsf versions. Only GSF 3.11 is supported."""

    _3_11 = GSF_LIBRARY_VERSION


class c_gsfNextJsonRecord(Structure):
    _fields_ = [("last_return_value", c_int), ("json_record", c_char_p)]


class Gsf:
    def __init__(self, gsf_version: GsfVersion = GsfVersion._3_11):
        host_system = system()
        host_arch = machine()
        if host_system != "Linux":
            raise OSError(
                f"bluemvmt-gsf supports Linux only; current platform is {host_system}."
            )
        if host_arch not in SUPPORTED_ARCHITECTURES:
            raise OSError(
                "bluemvmt-gsf supports Linux architectures "
                f"{', '.join(SUPPORTED_ARCHITECTURES)}; current architecture is "
                f"{host_arch}."
            )

        self._libgsf_abs_path = str(
            Path(__file__).parent / "lib" / f"libgsf-{host_arch}-{gsf_version.value}.so"
        )
        try:
            self._libgsf = CDLL(self._libgsf_abs_path)
        except OSError as osex:
            raise OSError(
                f"Cannot load bundled libgsf from {self._libgsf_abs_path}. "
                f"Expected GSF {gsf_version.value} for Linux {host_arch} "
                f"(Python {sys.version_info.major}.{sys.version_info.minor}). "
                "Ensure the package was installed with its native library files "
                "and that the host glibc is new enough for the bundled binary."
            ) from osex

        self._libgsf.gsfClose.argtypes = [c_int]
        self._libgsf.gsfClose.restype = c_int

        self._libgsf.gsfOpen.argtypes = [c_char_p, c_int, POINTER(c_int)]
        self._libgsf.gsfOpen.restype = c_int

        self._libgsf.gsfOpenBuffered.argtypes = [
            c_char_p,
            c_int,
            POINTER(c_int),
            c_int,
        ]
        self._libgsf.gsfOpenBuffered.restype = c_int

        self._libgsf.gsfOpenForJson.argtypes = [
            c_char_p,
            c_int,
            POINTER(c_int),
            c_int,
            c_int,
            c_int,
        ]
        self._libgsf.gsfOpenForJson.restype = c_int

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
        :param desired_record: bluemvmt_gsf.models.RecordType
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
