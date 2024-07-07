from importlib import import_module

from fastapi import APIRouter
from pydantic import ConfigDict, field_validator

from server.core.config import settings
from server.core.schemas import BaseSchema


class RouterConfig(BaseSchema):
    router: APIRouter
    config: dict = {"prefix": settings.API_PREFIX}

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator("router", mode="before")
    def validate_router(cls, v):
        try:
            module_name, class_name = f"{v}.routes", "router"
            module = import_module(module_name)
            router = getattr(module, class_name)
            return router
        except (ValueError, ImportError, AttributeError):
            raise ValueError(f"Invalid class path: {v}")
