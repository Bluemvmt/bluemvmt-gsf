"""
    Dummy conftest.py for bluemvmt_gsf.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    - https://docs.pytest.org/en/stable/fixture.html
    - https://docs.pytest.org/en/stable/writing_plugins.html
"""

import logging
import os

import pytest
from gsfpy3_09 import FileMode, open_gsf

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


@pytest.fixture(scope="session")
def swath_bathymetric_ping_json():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(f"{dir_path}/swath_bathymetric_ping.json") as f:
        yield f.read()


@pytest.fixture(scope="session")
def gsf_file_name():
    return "16mbs17076_211324_p_100.gsf"


@pytest.fixture(scope="session")
def gsf_test_file_path(gsf_file_name):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return f"{dir_path}/{gsf_file_name}"


@pytest.fixture(scope="function")
def gsf_file(gsf_test_file_path):
    with open_gsf(gsf_test_file_path, mode=FileMode.GSF_READONLY_INDEX) as gsf_file:
        yield gsf_file
