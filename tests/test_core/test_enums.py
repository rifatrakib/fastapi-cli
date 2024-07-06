import pytest

from server.core.enums import ConfigSource, Modes, Tags, Versions


def test_config_source_enum():
    assert ConfigSource.ENV.value == "env"
    assert ConfigSource.JSON.value == "json"

    assert ConfigSource("env") == ConfigSource.ENV
    assert ConfigSource("json") == ConfigSource.JSON

    with pytest.raises(ValueError):
        ConfigSource("invalid")


def test_modes_enum():
    assert Modes.DEVELOPMENT.value == "development"
    assert Modes.STAGING.value == "staging"
    assert Modes.PRODUCTION.value == "production"

    assert Modes("development") == Modes.DEVELOPMENT
    assert Modes("staging") == Modes.STAGING
    assert Modes("production") == Modes.PRODUCTION

    with pytest.raises(ValueError):
        Modes("invalid")


def test_tags_enum():
    assert Tags.HEALTH_CHECK.value == "Health Check"

    assert Tags("Health Check") == Tags.HEALTH_CHECK

    with pytest.raises(ValueError):
        Tags("invalid")


def test_versions_enum():
    assert Versions.VERSION_1.value == "v1"

    assert Versions("v1") == Versions.VERSION_1

    with pytest.raises(ValueError):
        Versions("invalid")
