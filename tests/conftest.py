# content of conftest.py

import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--runcloud", action="store_true", default=False, help="run cloud tests"
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "cloud: mark test as triggering cloud")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--runcloud"):
        # --runcloud given in cli: do not skip cloud tests
        return
    skip_cloud = pytest.mark.skip(reason="need --runcloud option to run")
    for item in items:
        if "cloud" in item.keywords:
            item.add_marker(skip_cloud)
