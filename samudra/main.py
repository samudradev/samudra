from pathlib import Path

import typer
from typer import Typer
from rich import print
from samudra.conf.database.core import get_database

from samudra.models import create_tables
from samudra.conf.database.options import DatabaseEngine

app = Typer()


@app.command()
def new(
    name: str = typer.Argument(..., rich_help_panel="Name of database."),
    path: str = typer.Option(".", rich_help_panel="Path to store database (SQLite)"),
    experimental: bool = typer.Option(
        False, rich_help_panel="Include experimental tables"
    ),
    engine: DatabaseEngine = typer.Option(
        DatabaseEngine.SQLite.value,
        "--engine",
        "-e",
        rich_help_panel="Engine to use for database.",
    ),
) -> None:
    """Creates a new database"""
    if path == "." and DatabaseEngine[engine] == DatabaseEngine.SQLite:
        db_path = input(
            "Please specify the folder to store database. Database will be stored in 'path/name/samudra.db'\nDefaults to '.':"
        )
    else:
        db_path = path
    database = get_database(db_name=name, engine=engine, path=db_path)
    tables = create_tables(
        database=database,
        auth=False,
        experimental=experimental,
    )
    # TODO Jot this down in some sort of internal list
    print(f"`samudra.db` has been created in {db_path} with the following tables:")
    [print("-", table) for table in tables]


@app.command()
def newer():
    pass


if __name__ == "__main__":
    app()
