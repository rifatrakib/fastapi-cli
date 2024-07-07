from unittest.mock import mock_open, patch

from server.core.config import settings
from server.core.documentation.openapi import api_configuration_options, configure_openapi
from server.core.documentation.schemas import APIConfig, Contact, ExternalDocs, OpenAPIConfig, OpenAPITags
from server.core.enums import Tags


def test_api_configuration_options():
    mock_description = "Test description from README.md"
    expected_contact = Contact(
        name="admin",
        url="https://example.com/",
        email="admin@example.com",
    )

    with patch("builtins.open", mock_open(read_data=mock_description)):
        api_config = api_configuration_options()

    assert isinstance(api_config, APIConfig)
    assert api_config.title == settings.APP_NAME
    assert api_config.description == mock_description
    assert api_config.version == settings.VERSION
    assert api_config.terms_of_service == "https://example.com/"
    assert api_config.contact == expected_contact
    assert api_config.openapi_url == f"{settings.API_PREFIX}/openapi.json"
    assert api_config.docs_url == f"{settings.API_PREFIX}/docs"
    assert api_config.redoc_url == f"{settings.API_PREFIX}/redoc"


def test_configure_openapi():
    mock_description = "Test description from README.md"
    expected_contact = Contact(
        name="admin",
        url="https://example.com/",
        email="admin@example.com",
    )
    expected_tags_metadata = [
        OpenAPITags(
            name=Tags.HEALTH_CHECK,
            description="Verify server operability and configuration variables.",
            externalDocs=ExternalDocs(
                description="Server Health Check",
                url="https://example.com/",
            ),
        ),
    ]

    with patch("builtins.open", mock_open(read_data=mock_description)):
        openapi_config = configure_openapi()

    assert isinstance(openapi_config, OpenAPIConfig)
    assert openapi_config.title == settings.APP_NAME
    assert openapi_config.description == mock_description
    assert openapi_config.version == settings.VERSION
    assert openapi_config.terms_of_service == "https://example.com/"
    assert openapi_config.contact == expected_contact
    assert openapi_config.openapi_url == f"{settings.API_PREFIX}/openapi.json"
    assert openapi_config.docs_url == f"{settings.API_PREFIX}/docs"
    assert openapi_config.redoc_url == f"{settings.API_PREFIX}/redoc"
    assert openapi_config.tags_metadata == expected_tags_metadata
