from fastapi import FastAPI

from server.core.config import services
from server.core.config.schemas import RouterConfig
from server.core.documentation.openapi import add_endpoint_description, configure_openapi
from server.core.documentation.schemas import OpenAPIConfig


def merge_routers(app: FastAPI) -> FastAPI:
    for name in services:
        service = RouterConfig(router=name)
        for route in service.router.routes:
            add_endpoint_description(route, name)
        app.include_router(service.router, **service.config)
    return app


def configure_app() -> FastAPI:
    api_config: OpenAPIConfig = configure_openapi()
    app = FastAPI(**api_config.model_dump())
    merge_routers(app)
    return app
