from pathlib import Path

import typer
from typer import Typer
from rich import print

from samudra.models import create_tables
from samudra.conf.local import save_database, get_databases_config
from samudra.conf.database.options import DatabaseEngine
from samudra.conf.database.core import get_database

app = Typer()


@app.command()
def create(
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
    database = get_database(db_name=name, engine=engine, path=path, new=True)
    tables = create_tables(
        database=database,
        auth=False,
        experimental=experimental,
    )
    save_database(db_name=name, path=Path(path))
    print(
        f"`samudra.db` has been created in {Path(path, name).resolve()} with the following tables:"
    )
    [print("-", table) for table in tables]


@app.command()
def list():
    """Lists available databases"""
    # TODO Print as tables
    print(get_databases_config()["databases"])
