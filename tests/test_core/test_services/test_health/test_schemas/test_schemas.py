import json

import pytest

from server.core.services.health.schemas.responses import HealthResponse


def test_health_response_schema():
    data = HealthResponse(
        APP_NAME="Test",
        VERSION="0.0.1",
        MODE="development",
        DEBUG=True,
    )

    assert data.APP_NAME == "Test"
    assert data.VERSION == "0.0.1"

    json_data = json.loads(data.model_dump_json(by_alias=True))
    assert "app_name" in json_data
    assert "version" in json_data


def test_health_response_wrong_enum_mode():
    with pytest.raises(ValueError):
        HealthResponse(
            APP_NAME="Test",
            VERSION="0.0.1",
            MODE="test",
            DEBUG=True,
        )
