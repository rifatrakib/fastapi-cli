from server.core.config import settings
from server.core.enums import Tags

from .schemas import APIConfig, Contact, ExternalDocs, OpenAPIConfig, OpenAPITags


def api_configuration_options() -> APIConfig:
    with open("server/README.md") as reader:
        description = reader.read()

    api_config = APIConfig(
        title=settings.APP_NAME,
        description=description,
        version=settings.VERSION,
        terms_of_service="https://example.com/",  # TODO: Update this URL with an actual terms of service
        # TODO: Update this contact information with the actual contact information for primary stakeholder
        contact=Contact(
            name="admin",
            url="https://example.com/",
            email="admin@example.com",
        ),
        openapi_url=f"{settings.API_PREFIX}/openapi.json",
        docs_url=f"{settings.API_PREFIX}/docs",
        redoc_url=f"{settings.API_PREFIX}/redoc",
    )
    return api_config


def configure_openapi() -> OpenAPIConfig:
    api_config: APIConfig = api_configuration_options()
    tags_metadata: list[OpenAPITags] = [
        OpenAPITags(
            name=Tags.HEALTH_CHECK,
            description="Verify server operability and configuration variables.",
            externalDocs=ExternalDocs(
                description="Server Health Check",
                url="https://example.com/",
            ),
        ),
    ]
    return OpenAPIConfig(**api_config.model_dump(), tags_metadata=tags_metadata)
