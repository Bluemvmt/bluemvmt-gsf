"""Shared pytest fixtures for bluemvmt-gsf."""

from pathlib import Path

import pytest

TEST_DIR = Path(__file__).resolve().parent
DEFAULT_GSF_FILE = "GSF3_09_test_file.gsf"


def pytest_addoption(parser):
    parser.addoption(
        "--test-gsf-file",
        action="store",
        default=DEFAULT_GSF_FILE,
        help="GSF fixture filename under tests/ (older formats remain readable).",
    )


@pytest.fixture(scope="session")
def gsf_file_name(request) -> str:
    return request.config.getoption("--test-gsf-file")


@pytest.fixture(scope="session")
def gsf_test_file_path(gsf_file_name) -> Path:
    return TEST_DIR / gsf_file_name


@pytest.fixture(scope="session")
def swath_bathymetric_ping_json() -> str:
    return (TEST_DIR / "swath_bathymetric_ping.json").read_text(encoding="utf-8")


@pytest.fixture(scope="session")
def processing_parameters_json() -> str:
    return (TEST_DIR / "processing_parameters.json").read_text(encoding="utf-8")


@pytest.fixture(scope="session")
def processing_parameters_flattened_json() -> str:
    return (TEST_DIR / "processing_parameters_flattened.json").read_text(
        encoding="utf-8"
    )
