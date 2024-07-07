from server.core.config.environments import AppConfig
from server.core.enums import Modes


class ProductionConfig(AppConfig):
    DEBUG: bool = False
    MODE: Modes = Modes.PRODUCTION
