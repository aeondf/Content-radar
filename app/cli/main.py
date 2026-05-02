import typer

from app.cli.seed import seed_sources

app = typer.Typer(help="Content radar admin CLI", no_args_is_help=True)


@app.callback()
def main() -> None:
    """Content Radar admin CLI."""


app.command(name="seed-sources")(seed_sources)


@app.command()
def hello() -> None:
    """Smoke-test command."""
    typer.echo("Hello from radar CLI!")


if __name__ == "__main__":
    app()
