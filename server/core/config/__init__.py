import os
from functools import lru_cache

from server.core.config.environments import AppConfig
from server.core.config.environments.development import DevelopmentConfig
from server.core.config.environments.production import ProductionConfig
from server.core.config.environments.staging import StagingConfig
from server.core.enums import Modes
from server.core.utils import read_secrets


class SettingsFactory:
    def __init__(self, mode: str):
        self.mode = mode

    def __call__(self) -> AppConfig:
        config_model = DevelopmentConfig
        if self.mode == Modes.STAGING:
            config_model = StagingConfig
        elif self.mode == Modes.PRODUCTION:
            config_model = ProductionConfig

        if os.getenv("ENV_SOURCE") == "json":
            secrets = read_secrets(self.mode)
            return config_model(**secrets)

        return config_model()


@lru_cache()
def get_settings(mode: Modes) -> AppConfig:
    factory = SettingsFactory(mode=mode)
    return factory()


settings: AppConfig = get_settings(mode=os.getenv("MODE", default="development"))
services: list[str] = [
    "server.core.services.health",
]
