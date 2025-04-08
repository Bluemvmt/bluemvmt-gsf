import sys


class Gsf:
    def __init__(self, version: str = "03.10"):
        self._version = version

    @property
    def version(self) -> str:
        return self._version

    @version.setter
    def version(self, value: str):
        self._version = value


gsf: Gsf = Gsf()