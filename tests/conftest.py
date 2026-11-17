from copy import deepcopy
from importlib import import_module

import pytest
from fastapi.testclient import TestClient


app_module = import_module("src.app")


@pytest.fixture
def activities(monkeypatch):
    test_activities = deepcopy(app_module.activities)
    monkeypatch.setattr(app_module, "activities", test_activities)
    return test_activities


@pytest.fixture
def client(activities):
    return TestClient(app_module.app)
