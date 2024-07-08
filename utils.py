import asyncio
from enum import Enum
from pathlib import Path

import aiofiles


class Methods(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"


async def write_service_file(asset_file: Path, project: str, registry: str, name: str):
    async with aiofiles.open(asset_file, "r") as file:
        text = await file.read()

    content = text.replace("{placeholder}", name).replace("{Placeholder}", name.capitalize())

    try:
        dir, file_name = str(asset_file).replace("\\", "/").replace("assets/service/", "").rsplit("/", 1)
        file_name = file_name.replace(".txt", ".py")
        dest = Path(f"{project}/server/{registry}/{name}/{dir}")
    except Exception:
        file_name = str(asset_file).replace("\\", "/").replace("assets/service/", "").replace(".txt", ".py")
        dest = Path(f"{project}/server/{registry}/{name}")

    dest.mkdir(parents=True, exist_ok=True)
    async with aiofiles.open(f"{dest}/{file_name}", "w") as file:
        await file.write(content)


async def generate_service_files(project: str, registry: str, service: str):
    source = Path("assets/service")
    files = [file for file in source.rglob("*") if file.is_file()]

    tasks = []
    for file in files:
        tasks.append(write_service_file(file, project, registry, service))

    await asyncio.gather(*tasks, return_exceptions=False)
    Path(f"{project}/server/{registry}/{service}/__init__.py").touch()
    Path(f"{project}/server/{registry}/{service}/routes/__init__.py").touch()
    Path(f"{project}/server/{registry}/{service}/schemas/__init__.py").touch()
    print("Services created successfully!")


async def append_endpoint(project: str, registry: str, service: str, version: str, method: str, path: str, fn: str):
    code_source = Path("assets/endpoint/function.txt")
    async with aiofiles.open(code_source, "r") as file:
        code = await file.read()

    description_source = Path("assets/endpoint/description.txt")
    async with aiofiles.open(description_source, "r") as file:
        description = await file.read()

    mapper = {
        "{method}": method.upper(),
        "{path}": path,
        "{function}": fn,
        "{version}": version,
        "{service}": service,
    }
    for key, value in mapper.items():
        code = code.replace(key, value)
        description = description.replace(key, value)

    code_file = Path(f"{project}/server/{registry}/{service}/routes/{version}.py")
    description_file = Path(f"{project}/server/{registry}/{service}/documentation/{fn}.md")
    description_file.touch()

    async with aiofiles.open(code_file, "a") as f:
        await f.write(code)

    async with aiofiles.open(description_file, "w") as f:
        await f.write(description)


def validate_methods(method_name: str):
    if method_name.upper() not in Methods.__members__.values():
        raise KeyError
