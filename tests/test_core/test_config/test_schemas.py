import pytest
from fastapi import APIRouter
from pydantic import ValidationError

from server.core.config import settings
from server.core.config.schemas import RouterConfig


def test_router_config_valid_router():
    config = RouterConfig(router="server.services.health")
    assert config.config == {"prefix": settings.API_PREFIX}
    assert isinstance(config.router, APIRouter)


def test_router_config_invalid_router_import_error():
    with pytest.raises(ValidationError):
        RouterConfig(router="invalid.module")


def test_router_config_invalid_router_attribute_error():
    with pytest.raises(ValidationError):
        RouterConfig(router="server.core")


def test_router_config_invalid_class_path():
    with pytest.raises(ValidationError):
        RouterConfig(router="invalid_class_path")
