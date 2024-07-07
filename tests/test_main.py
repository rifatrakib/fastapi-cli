from unittest.mock import MagicMock, patch

import pytest
from fastapi import APIRouter
from fastapi.testclient import TestClient

from server.core.config.services import configure_app


@pytest.fixture
def client():
    app = configure_app()
    return TestClient(app)


def test_app_routes(client):
    with patch("server.core.documentation.openapi.configure_openapi") as mock_configure_openapi, patch(
        "server.core.config.services.merge_routers"
    ) as mock_merge_routers:

        # Mock the OpenAPI configuration
        mock_api_config = MagicMock()
        mock_configure_openapi.return_value = mock_api_config

        # Mock the merge_routers to add a test route
        def mock_merge(app):
            router = APIRouter()

            @router.get("/test-route")
            async def test_route():
                return {"message": "Test route"}

            app.include_router(router)

        mock_merge_routers.side_effect = mock_merge

        # Initialize the app
        app = configure_app()
        client = TestClient(app)

        # Check if the test route is included
        routes = {route.path for route in app.routes}
        assert "/test-route" in routes

        # Make a request to the test route
        response = client.get("/test-route")
        assert response.status_code == 200
        assert response.json() == {"message": "Test route"}
