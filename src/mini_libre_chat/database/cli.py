import click

from mini_libre_chat.api.initialize import create_schema_and_tables, drop_schema


@click.group()
def cli():
    """Football Database - Store football data"""
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


if __name__ == "__main__":
    cli()
