import asyncio
import subprocess
import zipfile
from pathlib import Path

import typer

from utils import Methods, append_endpoint, generate_service_files, validate_methods

app = typer.Typer()


@app.command()
def check(name: str, option: str):
    typer.echo(f"Checking {name} {option}...")


@app.command(name="run")
def run_server():
    subprocess.run("uvicorn server.main:app --reload", shell=True)


@app.command(name="startproject")
def start_project(dir: str = typer.Argument(..., help="Directory to create the project")):
    Path(".env").touch()
    with open(".env", "w") as file:
        file.write("APP_NAME=MyApp\nMODE=development\nVERSION=0.0.1\nAPI_PREFIX=api\n")

    source = "assets/app.zip"
    dest = Path(dir)
    dest.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(source, "r") as zip:
        zip.extractall(dest)

    print("Project created successfully!\n")
    print("Create and activate a virtual environment and then run the following commands to run the app...\n")

    if dir != ".":
        print(f"cd {dir}")

    print("pip install poetry")
    print("poetry install")
    print("uvicorn server.main:app --reload\n")


@app.command(name="createapp")
def create_app(
    project: str = typer.Option(".", help="Name of the project"),
    registry: str = typer.Option("services", help="Name of the registry"),
    service: str = typer.Option(None, help="Name of the app"),
):
    if not any([project, registry, service]):
        typer.echo("Please provide all the required arguments")
        raise typer.Exit()

    asyncio.run(generate_service_files(project, registry, service))


@app.command(name="addendpoint")
def add_endpoint(
    project: str = typer.Option(".", help="Name of the project"),
    registry: str = typer.Option("services", help="Name of the registry"),
    service: str = typer.Option(None, help="Name of the service"),
    version: str = typer.Option(None, help="Version of the service"),
    method: Methods = typer.Option(None, help="HTTP method"),
    path: str = typer.Option(None, help="Path for the endpoint"),
    fn: str = typer.Option(None, help="Function name"),
):
    try:
        validate_methods(method)
        if not any([project, registry, service, version, method, path, fn]):
            typer.echo("Please provide all the required arguments")
            raise typer.Exit()

        asyncio.run(append_endpoint(project, registry, service, version, method, path, fn))
    except Exception as e:
        typer.echo(e)
        raise typer.Exit()


if __name__ == "__main__":
    app()
