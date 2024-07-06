from typing import Type

from pydantic import model_validator
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource
from typing_extensions import Self

from server.core.enums import ConfigSource, Modes
from server.core.schemas import BaseConfig
from server.core.types import OptionalInteger, OptionalString


class AppConfig(BaseConfig):
    APP_NAME: str
    MODE: Modes
    VERSION: str
    API_PREFIX: str
    ENV_SOURCE: ConfigSource = "env"

    # SQL database config
    RDS_USER: OptionalString = None
    RDS_PASSWORD: OptionalString = None
    RDS_HOST: OptionalString = None
    RDS_PORT: OptionalInteger = None
    RDS_NAME: OptionalString = None
    RDS_ENGINE: str = "sqlite+aiosqlite"

    # Cache config
    CACHE_USER: OptionalString = None
    CACHE_PASSWORD: OptionalString = None
    CACHE_HOST: OptionalString = None
    CACHE_PORT: OptionalInteger = None
    CACHE_NAME: OptionalString = None
    CACHE_ENGINE: OptionalString = "memory"

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        # add or remove sources from here.
        # refer to server/core/config/environments/sources/__init__.py for an example custom source
        sources = (
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
        )
        return sources

    @model_validator(mode="after")
    def validate_rds_config(self) -> Self:
        username = self.RDS_USER
        password = self.RDS_PASSWORD
        host = self.RDS_HOST
        port = self.RDS_PORT
        name = self.RDS_NAME
        engine = self.RDS_ENGINE

        # when using an SQLite database engine
        if engine.startswith("sqlite"):
            if any([username, password, host, port]):
                raise ValueError("SQLite does not require username, password, host, and port")

            if not name:
                self.RDS_NAME = ":memory:"
                return self
            else:
                if not name.startswith("./"):
                    raise ValueError("SQLite database name must start with './'")
                self.RDS_NAME = name if name.endswith(".sqlite") else f"{name}.sqlite"
                return self

        # when using other database engines
        if engine and not any([host, port, name]):
            raise ValueError(f"{engine.split('+')[0]} database engine requires host, port, and a database name")

        return self

    @model_validator(mode="after")
    def validate_cache_config(self) -> Self:
        username = self.CACHE_USER
        password = self.CACHE_PASSWORD
        host = self.CACHE_HOST
        port = self.CACHE_PORT
        engine = self.CACHE_ENGINE

        # when using locmem or memory cache services
        if engine.startswith("memory"):
            if any([username, password, host, port]):
                raise ValueError("In-memory cache does not require username, password, host, and port")
            return self

        # when using other cache services
        if engine and not any([host, port]):
            raise ValueError(f"{engine.split('+')[0]} cache service requires host and port")

        return self

    @property
    def RDS_URI(self) -> str:
        return self.prepare_resource_uri(
            username=self.RDS_USER,
            password=self.RDS_PASSWORD,
            host=self.RDS_HOST,
            port=self.RDS_PORT,
            name=self.RDS_NAME,
            engine=self.RDS_ENGINE,
            resource_type="database",
        )

    @property
    def CACHE_URI(self) -> str:
        return self.prepare_resource_uri(
            username=self.CACHE_USER,
            password=self.CACHE_PASSWORD,
            host=self.CACHE_HOST,
            port=self.CACHE_PORT,
            name=self.CACHE_NAME,
            engine=self.CACHE_ENGINE,
            resource_type="cache",
        )

    def prepare_resource_uri(
        self,
        username: OptionalString,
        password: OptionalString,
        host: OptionalString,
        port: OptionalInteger,
        name: OptionalString,
        engine: OptionalString,
        resource_type: str,
    ) -> str:
        # when all the required fields are given
        if all([username, password, host, port, engine]):
            domain = f"{username}:{password}@{host}:{port}"
            return f"{engine}://{domain}/{name}" if name else f"{engine}://{domain}"

        # when password is not given
        if all([username, host, port, engine]):
            domain = f"{username}@{host}:{port}"
            return f"{engine}://{domain}/{name}" if name else f"{engine}://{domain}"

        # when username and password are not given
        if all([host, port, engine]):
            domain = f"{host}:{port}"
            return f"{engine}://{domain}/{name}" if name else f"{engine}://{domain}"

        # when nothing is given except the name optionally
        if not any([username, password, host, port]):
            if resource_type == "database":
                return f"{engine}:///{name}"
            else:
                return f"{engine}://"
