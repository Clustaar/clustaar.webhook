import os
import pytest
from falcon import Request


PROJECT_PATH = os.path.join(os.path.dirname(__file__), "..")
PACKAGE_PATH = os.path.join(PROJECT_PATH, "src")
os.sys.path.insert(0, PROJECT_PATH)
os.sys.path.insert(0, PACKAGE_PATH)


def pytest_runtest_setup(item):
    # Reset falcon global var between each test
    # If not done we can't use a falcon testing client and create http request via Factory
    Request._wsgi_input_type_known = False
