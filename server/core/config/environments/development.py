from server.core.config.environments import AppConfig
from server.core.enums import Modes


class DevelopmentConfig(AppConfig):
    DEBUG: bool = True
    MODE: Modes = Modes.DEVELOPMENT
