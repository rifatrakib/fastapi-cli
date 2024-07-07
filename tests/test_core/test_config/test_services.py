from unittest.mock import MagicMock, patch

from fastapi import APIRouter, FastAPI

from server.core.config import services, settings
from server.core.config.services import configure_app, merge_routers


def test_merge_routers():
    app = FastAPI()

    # Mock the services
    mock_services = ["server.core.services.health"]
    services_backup = services.copy()
    services[:] = mock_services

    with patch("server.core.config.schemas.RouterConfig") as mock_router_config:
        mock_router1 = APIRouter()

        mock_service1 = MagicMock()
        mock_service1.router = mock_router1
        mock_service1.config = {"prefix": "/health"}

        mock_router_config.side_effect = [mock_service1]

        app = merge_routers(app)

        routes = {route.path for route in app.routes}
        assert f"{settings.API_PREFIX}/health" in routes

    # Restore the original services list
    services[:] = services_backup


def test_configure_app():
    app = configure_app()

    assert isinstance(app, FastAPI)
    assert app.title == settings.APP_NAME
    assert app.version == settings.VERSION
    assert app.openapi_url.startswith(settings.API_PREFIX)

    # Ensure merge_routers was called
    with patch("server.core.config.services.merge_routers") as mock_merge_routers:
        configure_app()
        mock_merge_routers.assert_called_once()
