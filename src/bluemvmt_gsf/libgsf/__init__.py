from ctypes import byref, c_int
from enum import IntEnum
from os import fsencode
from pathlib import Path
from typing import Optional, Union

from ..models import RecordType
from .bindings import (
    gsfClose,
    gsfGetNumberRecords,
    gsfIntError,
    gsfNextJsonRecord,
    gsfOpen,
    gsfOpenBuffered,
    gsfStringError,
)


class FileMode(IntEnum):
    GSF_READONLY = 2
    GSF_READONLY_INDEX = 4


class GsfException(Exception):
    """
    Generates an exception based on the last error code
    """

    def __init__(self):
        self._error_code = gsfIntError()
        self._error_message = gsfStringError().decode()
        super().__init__(f"[{self._error_code}] {self._error_message}")

    @property
    def error_code(self) -> int:
        return self._error_code

    @property
    def error_message(self) -> str:
        return self._error_message


class GsfFile:
    """
    Represents an open connection to a GSF file
    """

    def __init__(self, handle: c_int, desired_record: c_int = RecordType.GSF_NEXT_RECORD):
        self.handle = handle
        self.desired_record = desired_record

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """
        Once this method has been called further operations will fail
        :raises GsfException: Raised if anything went wrong
        """
        _handle_failure(gsfClose(self.handle))

    def next_json_record(
        self,
    ):
        
        next_record = gsfNextJsonRecord(self.handle, self.desired_record)
        while next_record.last_return_value > 0:
            yield next_record.json_record
            next_record = gsfNextJsonRecord(self.handle, self.desired_record)

    def get_number_records(self, desired_record: RecordType) -> int:
        """
        May only be used when the file is open for direct access (GSF_READONLY_INDEX or
        GSF_UPDATE_INDEX).
        :param desired_record: Specifies the type of record to count
        :return: Number of records of type desired_record, otherwise -1
        """
        count = gsfGetNumberRecords(self.handle, desired_record)
        _handle_failure(count)
        return count


def open_gsf(
    path: Union[str, Path],
    mode: int = FileMode.GSF_READONLY_INDEX,
    buffer_size: Optional[int] = None,
) -> GsfFile:
    """
    Factory function to create GsfFile objects
    :param path: Location of GSF file to open
    :param mode: Mode to open the file in (read-only by default)
    :param buffer_size: If a value is provided then a buffer will be used to read the
                        file
    :return: Object representing the open connection to the specified file
    :raises GsfException: Raised if anything went wrong
    """
    handle = c_int(0)

    if isinstance(path, Path):
        path = str(path)

    _handle_failure(
        gsfOpen(fsencode(path), mode, byref(handle))
        if buffer_size is None
        else gsfOpenBuffered(path.encode(), mode, byref(handle), buffer_size)
    )

    return GsfFile(handle)


_ERROR_CODE = -1


def _handle_failure(return_code: int):
    """
    Error handling logic
    :param return_code: The return code from one of functions in the gsfpy3_08.bindings
                        package
    """
    if return_code == _ERROR_CODE:
        raise GsfException()
