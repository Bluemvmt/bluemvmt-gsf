"""Decode Generic Sensor Format (GSF) files into Pydantic models."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("bluemvmt-gsf")
except PackageNotFoundError:  # pragma: no cover - editable/source tree fallback
    __version__ = "0.5.0"

__all__ = ["__version__"]
