from ctypes import byref, c_int
from enum import IntEnum
from os import fsencode
from pathlib import Path
from typing import Optional, Union

from ..models import RecordType
from .bindings import Gsf, GsfVersion


class FileMode(IntEnum):
    GSF_READONLY = 2
    GSF_READONLY_INDEX = 4


class GsfFile:
    """
    Represents an open connection to a GSF file
    """

    def __init__(
        self,
        path: Union[str, Path],
        include_denormalized_fields: bool = False,
        mode: int = FileMode.GSF_READONLY_INDEX,
        desired_record: c_int = RecordType.GSF_NEXT_RECORD,
        gsf_version: GsfVersion = GsfVersion._3_10,
        buffer_size: Optional[int] = None,
    ):
        self.gsf = Gsf(gsf_version=gsf_version)
        self.desired_record = desired_record
        self.include_denormalized_fields: int = 0
        if include_denormalized_fields is True:
            self.include_denormalized_fields = 1

        if isinstance(path, Path):
            self.path = str(path)
        else:
            self.path = path

        self.handle = c_int(0)
        if buffer_size is None:
            retvalue: int = self.gsf.gsfOpen(fsencode(self.path), mode, byref(self.handle))
        else:
            retvalue: int = self.gsf.gsfOpenBuffered(
                self.path.encode(), mode, byref(self.handle), buffer_size
            )

        self._handle_failure(retvalue)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """
        Once this method has been called further operations will fail
        :raises GsfException: Raised if anything went wrong
        """
        self._handle_failure(self.gsf.gsfClose(self.handle))

    def next_json_record(self, desired_record: int = 0):
        next_record = self.gsf.gsfNextJsonRecord(self.handle, desired_record, self.include_denormalized_fields )
        while next_record.last_return_value > 0:
            yield next_record.json_record
            next_record = self.gsf.gsfNextJsonRecord(self.handle, desired_record, self.include_denormalized_fields)

    def get_number_records(self, desired_record: RecordType) -> int:
        """
        May only be used when the file is open for direct access (GSF_READONLY_INDEX or
        GSF_UPDATE_INDEX).
        :param desired_record: Specifies the type of record to count
        :return: Number of records of type desired_record, otherwise -1
        """
        count = self.gsf.gsfGetNumberRecords(self.handle, desired_record)
        self._handle_failure(count)
        return count

    def _handle_failure(self, return_code: int):
        """
        Error handling logic
        :param return_code: The return code from the libgsf functions.
        """
        if return_code < 0:
            raise GsfException(self.gsf)


class GsfException(Exception):
    """
    Generates an exception based on the last error code
    """

    def __init__(self, gsf: Gsf):
        self._error_code = gsf.gsfIntError()
        self._error_message = gsf.gsfStringError().decode()
        super().__init__(f"[{self._error_code}] {self._error_message}")

    @property
    def error_code(self) -> int:
        return self._error_code

    @property
    def error_message(self) -> str:
        return self._error_message
