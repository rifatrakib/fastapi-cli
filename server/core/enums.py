from enum import Enum


class ConfigSource(str, Enum):
    ENV = "env"
    JSON = "json"


class Modes(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class Tags(str, Enum):
    HEALTH_CHECK = "Health Check"


class Versions(str, Enum):
    VERSION_1 = "v1"
