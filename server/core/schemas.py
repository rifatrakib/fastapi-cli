from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        str_strip_whitespace=True,
        use_enum_values=True,
        alias_generator=str.lower,
        json_encoders={
            datetime: lambda dt: dt.replace(tzinfo=timezone.utc).isoformat(),
        },
    )


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        env_file=".env",
        extra="forbid",
    )


class BaseRequestSchema(BaseSchema):
    model_config = ConfigDict(
        extra="forbid",
    )


class BaseResponseSchema(BaseSchema):
    pass
