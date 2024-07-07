from server.core.config.environments import AppConfig
from server.core.enums import Modes


class StagingConfig(AppConfig):
    DEBUG: bool = True
    MODE: Modes = Modes.STAGING
