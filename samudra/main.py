import os

import peewee
from typer import Typer
from rich import print

from samudra.models import create_tables

app = Typer()


@app.command()
def new(
    db_name: str = "samudra.db",
    path: str = ".",
    foreign_lang: bool = True,
    experimental: bool = False,
) -> None:
    """Creates a new local database

    Args:
        db_name (str, optional): name of database. Defaults to 'samudra.db'
        path (str, optional): path to store database. Defaults to '.
    """
    if path == ".":
        db_path = db_name
    tables = create_tables(
        database=peewee.SqliteDatabase(db_path),
        auth=False,
        foreign_lang=foreign_lang,
        experimental=experimental,
    )
    print(f"In {db_path}, Tables created: {tables} ")


@app.command()
def newer():
    pass


if __name__ == "__main__":
    app()
