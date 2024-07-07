from server.core.schemas import BaseSchema


class Contact(BaseSchema):
    name: str
    url: str
    email: str


class APIConfig(BaseSchema):
    title: str
    description: str
    version: str
    terms_of_service: str
    contact: Contact
    openapi_url: str
    docs_url: str
    redoc_url: str


class ExternalDocs(BaseSchema):
    description: str
    url: str


class OpenAPITags(BaseSchema):
    name: str
    description: str
    externalDocs: ExternalDocs


class OpenAPIConfig(APIConfig):
    tags_metadata: list[OpenAPITags]
