import typer

app = typer.Typer()


@app.command()
def check(name: str):
    typer.echo(f"Checking {name}...")


if __name__ == "__main__":
    app()
