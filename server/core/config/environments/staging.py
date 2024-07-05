from server.core.config.environments import AppConfig


class StagingConfig(AppConfig):
    DEBUG: bool = True
    MODE: str = "staging"
