"""
    Dummy contest.py for bluemvmt_gsf.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    - https://docs.pytest.org/en/stable/fixture.html
    - https://docs.pytest.org/en/stable/writing_plugins.html
"""

import logging
import os

import pytest
from bluemvmt_gsf.libgsf import open_gsf

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


def pytest_addoption(parser):
    parser.addoption("--save-json", action="store", default="false")
    parser.addoption("--test-gsf-file", action="store", default="GSF3_09_test_file.gsf")
    parser.addoption("--output-rec", action="store", default="false")


@pytest.fixture(scope="session")
def save_json(request) -> bool:
    return request.config.getoption("--save-json").lower() == "true"


@pytest.fixture(scope="session")
def output_rec(request) -> bool:
    return request.config.getoption("--output-rec").lower() == "true"


@pytest.fixture(scope="session")
def swath_bathymetric_ping_json():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(f"{dir_path}/swath_bathymetric_ping.json") as f:
        yield f.read()


@pytest.fixture(scope="session")
def gsf_file_name(request):
    return request.config.getoption("--test-gsf-file")


@pytest.fixture(scope="session")
def gsf_test_file_path(gsf_file_name):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return f"{dir_path}/{gsf_file_name}"


@pytest.fixture(scope="function")
def gsf_file(gsf_test_file_path):
    with open_gsf(gsf_test_file_path) as gsf_file:
        yield gsf_file
