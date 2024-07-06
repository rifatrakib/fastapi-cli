import json
import os
from json.decoder import JSONDecodeError
from typing import Any


def read_secrets(mode: str) -> dict[str, Any]:
    try:
        mode = os.getenv("MODE", default="development")
        with open(f"secrets/{mode}.json", "r") as reader:
            secrets = json.loads(reader.read())
        return secrets
    except FileNotFoundError:
        return {}
    except JSONDecodeError:
        return {}
