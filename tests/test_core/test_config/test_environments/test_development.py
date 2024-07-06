from server.core.config.environments.development import DevelopmentConfig
from server.core.enums import ConfigSource, Modes


def test_development_config_initialization():
    config = DevelopmentConfig(
        APP_NAME="TestApp",
        MODE=Modes.DEVELOPMENT,
        VERSION="1.0",
        API_PREFIX="/api",
    )

    # Check inherited attributes
    assert config.APP_NAME == "TestApp"
    assert config.MODE == Modes.DEVELOPMENT
    assert config.VERSION == "1.0"
    assert config.API_PREFIX == "/api"
    assert config.ENV_SOURCE == ConfigSource.ENV

    # Check DevelopmentConfig specific attributes
    assert config.DEBUG is True
    assert config.MODE == "development"
