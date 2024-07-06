import json
import os
from unittest.mock import mock_open, patch

import pytest
from pydantic_settings import BaseSettings

from server.core.config.environments.sources import JsonSettingsSource


# Define a mock settings class for testing
class MockSettings(BaseSettings):
    APP_NAME: str
    MODE: str
    VERSION: str
    API_PREFIX: str


@pytest.fixture
def mock_secrets_file():
    secrets = {
        "APP_NAME": "TestApp",
        "MODE": "development",
        "VERSION": "1.0",
        "API_PREFIX": "/api",
    }
    with patch("builtins.open", mock_open(read_data=json.dumps(secrets))):
        yield


@patch.dict(os.environ, {"MODE": "development"})
def test_read_secrets(mock_secrets_file):
    source = JsonSettingsSource(settings_cls=MockSettings)
    secrets = source.read_secrets()
    assert secrets == {
        "APP_NAME": "TestApp",
        "MODE": "development",
        "VERSION": "1.0",
        "API_PREFIX": "/api",
    }


@patch.dict(os.environ, {"MODE": "development"})
def test_call_method(mock_secrets_file):
    source = JsonSettingsSource(settings_cls=MockSettings)
    settings_dict = source()
    assert source.get_field_value("", "") is None
    assert settings_dict == {
        "APP_NAME": "TestApp",
        "MODE": "development",
        "VERSION": "1.0",
        "API_PREFIX": "/api",
    }
