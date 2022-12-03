from pathlib import Path

import typer
from rich import print
from typer import Typer

from samudra.conf.database.core import get_database, set_active_database
from samudra.conf.database.options import DatabaseEngine
from samudra.conf.local import read_databases_list
from samudra.models import create_tables

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
    database = get_database(name=name, engine=engine, path=path, new=True)
    tables = create_tables(
        database=database,
        auth=False,
        experimental=experimental,
    )
    print(
        f"`samudra.db` has been created in {Path(path, name).resolve()} with the following tables:"
    )
    [print("-", table) for table in tables]


@app.command()
def set(name: str = typer.Argument(..., rich_help_panel="Name of database")) -> None:
    """Sets an active database"""
    set_active_database(name=name)
    print(f"The active database has been set to `{name}`")


@app.command()
def list():
    """Lists available databases"""
    # TODO Print as tables
    print(read_databases_list()["databases"])
