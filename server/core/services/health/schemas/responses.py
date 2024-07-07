from server.core.enums import Modes
from server.core.schemas import BaseSchema


class HealthResponse(BaseSchema):
    APP_NAME: str
    VERSION: str
    MODE: Modes
    DEBUG: bool
