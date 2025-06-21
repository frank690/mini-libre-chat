"""
Command Line Interface for Mini Libre Chat
"""

import click
import uvicorn
from mini_libre_chat.database.initialize import create_schema_and_tables, drop_schema


@click.group()
def cli():
    pass


@cli.command()
def initialize():
    """Initialize the database (creates schema and tables)."""
    click.echo("Initializing database...")
    was_successful = create_schema_and_tables()

    if was_successful is True:
        click.echo("Database initialization successful!")
    else:
        click.echo("Database initialization failed!")


@cli.command()
def deconstruct():
    """Deconstruct the database (delete schema and all its tables)."""
    confirmation = click.prompt(
        "Are you sure you want to DELETE the schema and its tables?", type=str
    )

    if confirmation.upper() in ["YES", "Y"]:
        click.echo("Deconstructing database...")
        was_successful = drop_schema(confirmation=True)

        if was_successful is True:
            click.echo("Deconstructing database successfully!")
        else:
            click.echo("Deconstructing database failed!")


@cli.command()
@click.option("--host", default="127.0.0.1", help="Host address to bind.")
@click.option("--port", default=8000, help="Port to serve on.")
@click.option("--reload", is_flag=True, help="Enable auto-reload.")
def start(host, port, reload):
    """Start the FastAPI server."""
    uvicorn.run(
        "mini_libre_chat.api.main:app",
        host=host,
        port=port,
        reload=reload,
        factory=False,
    )


if __name__ == "__main__":
    cli()
