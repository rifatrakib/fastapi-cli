"""
Here is a custom source for PydanticBaseSettingsSource
that reads secrets from a JSON file which is named after
the MODE environment variable inside the secrets directory.
"""

import json
import os
from typing import Any

from pydantic_settings import PydanticBaseSettingsSource


class JsonSettingsSource(PydanticBaseSettingsSource):
    def read_secrets(self) -> dict[str, Any]:
        with open(f"secrets/{os.getenv('MODE')}.json") as f:
            return json.load(f)

    def __call__(self) -> dict[str, Any]:
        d: dict[str, Any] = {}
        secrets = self.read_secrets()

        for name in self.settings_cls.model_fields.keys():
            value = secrets.get(name)
            if value is not None:
                d[name] = value

        return d
