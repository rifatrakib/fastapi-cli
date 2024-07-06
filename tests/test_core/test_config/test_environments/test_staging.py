from server.core.config.environments.staging import StagingConfig
from server.core.enums import ConfigSource, Modes


def test_staging_config_initialization():
    config = StagingConfig(
        APP_NAME="TestApp",
        MODE=Modes.STAGING,
        VERSION="1.0",
        API_PREFIX="/api",
    )

    # Check inherited attributes
    assert config.APP_NAME == "TestApp"
    assert config.MODE == Modes.STAGING
    assert config.VERSION == "1.0"
    assert config.API_PREFIX == "/api"
    assert config.ENV_SOURCE == ConfigSource.ENV

    # Check DevelopmentConfig specific attributes
    assert config.DEBUG is True
    assert config.MODE == "staging"
