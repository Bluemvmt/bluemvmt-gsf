import json
from ctypes import byref, c_int
from enum import IntEnum
from os import fsencode
from pathlib import Path
from typing import Iterator, Union

from ..models import RecordType
from .bindings import Gsf, GsfVersion


class FileMode(IntEnum):
    GSF_READONLY = 2
    GSF_READONLY_INDEX = 4


class GsfFile:
    """
    Represents an open connection to a GSF file.
    """

    def __init__(
        self,
        path: Union[str, Path],
        include_denormalized_fields: bool = False,
        flatten: bool = False,
        mode: int = FileMode.GSF_READONLY_INDEX,
        gsf_version: GsfVersion = GsfVersion._3_11,
        buffer_size: int = 0,
    ):
        self.gsf = Gsf(gsf_version=gsf_version)
        self.include_denormalized_fields: int = 1 if include_denormalized_fields else 0
        self.flatten: int = 1 if flatten else 0
        self.path = str(path)
        self.buffer_size = buffer_size

        self.handle = c_int(0)
        retvalue: int = self.gsf.gsfOpenForJson(
            fsencode(self.path),
            mode,
            byref(self.handle),
            self.buffer_size,
            self.include_denormalized_fields,
            self.flatten,
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

    def next_json_record(
        self, desired_record: int = RecordType.GSF_NEXT_RECORD
    ) -> Iterator[bytes]:
        """
        Yield JSON records from the open GSF file.

        When ``desired_record`` is not ``GSF_NEXT_RECORD``, records are filtered
        in Python after decoding. Native libgsf filtering is unreliable across
        the bundled JSON helpers, so this wrapper guarantees the requested type.
        """
        next_record = self.gsf.gsfNextJsonRecord(
            self.handle, RecordType.GSF_NEXT_RECORD
        )
        while next_record.last_return_value > 0:
            payload = next_record.json_record
            if payload is not None:
                if (
                    desired_record == RecordType.GSF_NEXT_RECORD
                    or self._record_type(payload) == desired_record
                ):
                    yield payload
            next_record = self.gsf.gsfNextJsonRecord(
                self.handle, RecordType.GSF_NEXT_RECORD
            )

    @staticmethod
    def _record_type(payload: bytes) -> int:
        data = json.loads(payload)
        return int(data["record_type"])

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
