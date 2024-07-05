from server.core.config.environments import AppConfig


class ProductionConfig(AppConfig):
    DEBUG: bool = False
    MODE: str = "production"
