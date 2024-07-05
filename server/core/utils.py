import json
import os
from typing import Any


def read_secrets(mode: str) -> dict[str, Any]:
    mode = os.getenv("MODE", default="development")
    with open(f"secrets/{mode}.json", "r") as reader:
        secrets = json.loads(reader.read())
    return secrets
