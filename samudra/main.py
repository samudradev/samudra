from pathlib import Path

import peewee
import typer
from typer import Typer
from rich import print

from samudra.models import create_tables

app = Typer()


@app.command()
def new(
    db_name: str = typer.Argument(..., rich_help_panel="Name of database."),
    path: str = typer.Option(".", rich_help_panel="Path to store database"),
    experimental: bool = typer.Option(
        False, rich_help_panel="Include experimental tables"
    ),
) -> None:
    """Creates a new local database"""
    db_path = db_name if path == "." else Path(path, db_name).resolve()
    tables = create_tables(
        database=peewee.SqliteDatabase(db_path),
        auth=False,
        experimental=experimental,
    )
    # TODO Jot this down in some sort of internal list
    print(f"In {db_path}, Tables created: {tables} ")


@app.command()
def newer():
    pass


if __name__ == "__main__":
    app()
