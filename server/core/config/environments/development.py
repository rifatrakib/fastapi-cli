from server.core.config.environments import AppConfig


class DevelopmentConfig(AppConfig):
    DEBUG: bool = True
    MODE: str = "development"
