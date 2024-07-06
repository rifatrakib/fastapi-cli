import json
import os
from datetime import datetime, timezone
from unittest.mock import mock_open, patch

import pytest

from server.core.schemas import BaseConfig, BaseRequestSchema, BaseResponseSchema, BaseSchema


# Test BaseSchema JSON Encoders
def test_baseschema_json_encoders():
    class TestSchema(BaseSchema):
        timestamp: datetime

    dt = datetime(2024, 7, 5, 12, 30, 0, tzinfo=timezone.utc)
    schema = TestSchema(timestamp=dt)
    expected_iso_format = dt.replace(tzinfo=timezone.utc).isoformat()
    assert json.loads(schema.model_dump_json()) == {"timestamp": expected_iso_format}


# Test BaseSchema Configuration Dict
def test_baseschema_config_dict():
    class TestSchema(BaseSchema):
        pass

    config = TestSchema.model_config
    assert config.get("from_attributes") is True
    assert config.get("populate_by_name") is True
    assert config.get("str_strip_whitespace") is True
    assert config.get("use_enum_values") is True


# Test BaseConfig with Temporary .env File
@pytest.fixture
def temporary_env_file():
    env_vars = {"KEY": "value"}
    env_content = "\n".join(f"{key}={value}" for key, value in env_vars.items())

    with patch("builtins.open", mock_open(read_data=env_content)):
        with patch.dict(os.environ, env_vars):
            yield


def test_baseconfig_settings(temporary_env_file):
    class TestConfig(BaseConfig):
        KEY: str

    config = TestConfig()
    assert config.KEY == "value"
    assert config.model_config.get("env_file_encoding") == "utf-8"
    assert config.model_config.get("extra") == "forbid"


# Test BaseRequestSchema Configuration Dict
def test_base_request_schema_config_dict():
    class TestRequestSchema(BaseRequestSchema):
        pass

    config = TestRequestSchema.model_config
    assert config.get("extra") == "forbid"


# Test BaseResponseSchema Inheritance
def test_base_response_schema_inheritance():
    class TestResponseSchema(BaseResponseSchema):
        pass

    config = TestResponseSchema.model_config
    assert config.get("from_attributes") is True
    assert config.get("populate_by_name") is True
    assert config.get("str_strip_whitespace") is True
    assert config.get("use_enum_values") is True
