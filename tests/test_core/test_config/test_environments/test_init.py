import pytest
from pydantic import ValidationError

from server.core.config.environments import AppConfig
from server.core.enums import ConfigSource, Modes


def test_app_config_initialization():
    config = AppConfig(
        APP_NAME="TestApp",
        MODE=Modes.DEVELOPMENT,
        VERSION="1.0",
        API_PREFIX="/api",
    )
    assert config.APP_NAME == "TestApp"
    assert config.MODE == Modes.DEVELOPMENT
    assert config.VERSION == "1.0"
    assert config.API_PREFIX == "/api"
    assert config.ENV_SOURCE == ConfigSource.ENV


def test_sqlite_config_validation():
    config = AppConfig(
        APP_NAME="TestApp", MODE=Modes.DEVELOPMENT, VERSION="1.0", API_PREFIX="/api", RDS_ENGINE="sqlite+aiosqlite", RDS_NAME="./test_db"
    )
    assert config.RDS_NAME == "./test_db.sqlite"

    with pytest.raises(ValidationError):
        AppConfig(
            APP_NAME="TestApp",
            MODE=Modes.DEVELOPMENT,
            VERSION="1.0",
            API_PREFIX="/api",
            RDS_ENGINE="sqlite+aiosqlite",
            RDS_NAME="test_db",  # Name not starting with "./"
        )


def test_other_db_config_validation():
    with pytest.raises(ValidationError):
        AppConfig(APP_NAME="TestApp", MODE=Modes.DEVELOPMENT, VERSION="1.0", API_PREFIX="/api", RDS_ENGINE="postgresql+asyncpg")

    config = AppConfig(
        APP_NAME="TestApp",
        MODE=Modes.DEVELOPMENT,
        VERSION="1.0",
        API_PREFIX="/api",
        RDS_ENGINE="postgresql+asyncpg",
        RDS_USER="user",
        RDS_PASSWORD="pass",  # pragma: allowlist secret
        RDS_HOST="localhost",
        RDS_PORT=5432,
        RDS_NAME="test_db",
    )
    assert config.RDS_HOST == "localhost"


def test_memory_cache_config_validation():
    config = AppConfig(APP_NAME="TestApp", MODE=Modes.DEVELOPMENT, VERSION="1.0", API_PREFIX="/api", CACHE_ENGINE="memory")
    assert config.CACHE_ENGINE == "memory"

    with pytest.raises(ValidationError):
        AppConfig(APP_NAME="TestApp", MODE=Modes.DEVELOPMENT, VERSION="1.0", API_PREFIX="/api", CACHE_ENGINE="memory", CACHE_USER="user")


def test_other_cache_config_validation():
    with pytest.raises(ValidationError):
        AppConfig(APP_NAME="TestApp", MODE=Modes.DEVELOPMENT, VERSION="1.0", API_PREFIX="/api", CACHE_ENGINE="redis")

    config = AppConfig(
        APP_NAME="TestApp",
        MODE=Modes.DEVELOPMENT,
        VERSION="1.0",
        API_PREFIX="/api",
        CACHE_ENGINE="redis",
        CACHE_HOST="localhost",
        CACHE_PORT=6379,
    )
    assert config.CACHE_HOST == "localhost"


def test_rds_uri():
    config = AppConfig(
        APP_NAME="TestApp",
        MODE=Modes.DEVELOPMENT,
        VERSION="1.0",
        API_PREFIX="/api",
        RDS_ENGINE="postgresql+asyncpg",
        RDS_USER="user",
        RDS_PASSWORD="pass",  # pragma: allowlist secret
        RDS_HOST="localhost",
        RDS_PORT=5432,
        RDS_NAME="test_db",
    )
    assert config.RDS_URI == "postgresql+asyncpg://user:pass@localhost:5432/test_db"  # pragma: allowlist secret


def test_rds_uri_no_password():
    config = AppConfig(
        APP_NAME="TestApp",
        MODE=Modes.DEVELOPMENT,
        VERSION="1.0",
        API_PREFIX="/api",
        RDS_ENGINE="postgresql+asyncpg",
        RDS_USER="user",
        RDS_HOST="localhost",
        RDS_PORT=5432,
        RDS_NAME="test_db",
    )
    assert config.RDS_URI == "postgresql+asyncpg://user@localhost:5432/test_db"


def test_rds_uri_no_param():
    config = AppConfig(
        APP_NAME="TestApp",
        MODE=Modes.DEVELOPMENT,
        VERSION="1.0",
        API_PREFIX="/api",
    )
    assert config.RDS_URI == "sqlite+aiosqlite:///:memory:"


def test_rds_uri_only_name():
    config = AppConfig(
        APP_NAME="TestApp",
        MODE=Modes.DEVELOPMENT,
        VERSION="1.0",
        API_PREFIX="/api",
        RDS_NAME="./test_db",
    )
    assert config.RDS_URI == "sqlite+aiosqlite:///./test_db.sqlite"


def test_rds_uri_sqlite_fail():
    with pytest.raises(ValidationError):
        AppConfig(
            APP_NAME="TestApp",
            MODE=Modes.DEVELOPMENT,
            VERSION="1.0",
            API_PREFIX="/api",
            RDS_ENGINE="sqlite+aiosqlite",
            RDS_HOST="localhost",
        )


def test_cache_uri():
    config = AppConfig(
        APP_NAME="TestApp",
        MODE=Modes.DEVELOPMENT,
        VERSION="1.0",
        API_PREFIX="/api",
        CACHE_ENGINE="redis",
        CACHE_HOST="localhost",
        CACHE_PORT=6379,
    )
    assert config.CACHE_URI == "redis://localhost:6379"


def test_cache_uri_no_config():
    config = AppConfig(
        APP_NAME="TestApp",
        MODE=Modes.DEVELOPMENT,
        VERSION="1.0",
        API_PREFIX="/api",
    )
    assert config.CACHE_URI == "memory://"


def test_custom_sources():
    config = AppConfig(
        APP_NAME="TestApp",
        MODE=Modes.DEVELOPMENT,
        VERSION="1.0",
        API_PREFIX="/api",
    )
    sources = config.settings_customise_sources(
        AppConfig, None, None, None, None  # init_settings  # env_settings  # dotenv_settings  # file_secret_settings
    )
    assert len(sources) == 4
