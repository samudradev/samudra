import logging
import os
from contextvars import ContextVar
from pathlib import Path

import peewee as pw

from conf.local import (
    read_database_info,
    write_config,
    read_config,
    append_database_list,
)
from models.base import database_proxy
from samudra.conf.database.options import DatabaseEngine

db_state_default = {"closed": None, "conn": None, "ctx": None, "transactions": None}
db_state = ContextVar("db_state", default=db_state_default.copy())


class SQLiteConnectionState(pw._ConnectionState):
    """Defaults to make SQLite DB async-compatible (according to FastAPI/Pydantic)"""

    def __init__(self, **kwargs):
        super().__setattr__("_state", db_state)
        super().__init__(**kwargs)

    def __setattr__(self, name, value):
        self._state.get()[name] = value

    def __getattr__(self, name):
        return self._state.get()[name]


def set_active_database(name: str) -> None:
    """Sets the database as the currently active database"""
    # Check if the name is already registered in .samudra/databases.toml
    db_obj = read_database_info(name=name)
    if db_obj is None:
        raise FileNotFoundError(
            f"The database name `{name}` is not found. Perhaps it is not created yet."
        )
    # Write the info in .samudra/config.toml
    write_config({"active": name})
    # TODO ? Write relevant variables into .env for server?


def new_database(name: str, engine: DatabaseEngine, path: str) -> pw.Database:
    """Create and register a SQLite database or just register a database if not SQLite"""
    # ? Should this be a function parameters?
    DATABASE_HOST = os.getenv("DATABASE_HOST")
    DATABASE_PORT = int(os.getenv("DATABASE_PORT"))
    DATABASE_OPTIONS = os.getenv("DATABASE_OPTIONS")
    USERNAME = os.getenv("DATABASE_USERNAME")
    PASSWORD = os.getenv("DATABASE_PASSWORD")
    SSL_MODE = os.getenv("SSL_MODE")
    if engine is None or engine not in DatabaseEngine.__members__.values():
        raise ValueError(
            "Invalid engine. You entered {}. Valid values are: \n - {}".format(
                engine, "\n - ".join(DatabaseEngine.__members__.values())
            )
        )
    if engine == DatabaseEngine.SQLite:
        return create_sqlite(name=name, path=Path(path))
    if engine == DatabaseEngine.MySQL:
        conn_str = f"mysql://{USERNAME}:{PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{name}?ssl-mode=REQUIRED"
        return_db = pw.MySQLDatabase(conn_str)
        append_database_list(name=name, path=conn_str, engine=engine)
        logging.info(f"Connecting to {return_db.database} as {USERNAME}")
    else:
        raise NotImplementedError("Invalid engine")


def get_active_database() -> pw.Database:
    active_database_name = read_config(key="active")
    if not active_database_name:
        raise KeyError("No active database is defined")
    return get_database(name=active_database_name)


def get_database(name: str) -> pw.Database:
    """Returns the connection class based on the name."""
    info = read_database_info(name)
    if info.get("engine") == DatabaseEngine.SQLite:
        return_db = pw.SqliteDatabase(info.get("path"))
        return_db._state = SQLiteConnectionState()
        return return_db
    if info.get("engine") == DatabaseEngine.MySQL:
        return pw.MySQLDatabase(info.get("path"))


def create_sqlite(
    name: str, path: Path, filename: str = "samudra.db", description: str = ""
) -> pw.SqliteDatabase:
    base_path: Path = Path(path, name)
    full_path: Path = Path(base_path, filename)
    # Check if the given path is occupied.
    # If not occupied, create the database.
    # If occupied, raise FileExistsError.
    try:
        base_path.mkdir(parents=True)
    except FileExistsError:
        if full_path in [*base_path.iterdir()]:
            raise FileExistsError(
                f"A samudra database already exists in {full_path.resolve()}"
            )
        elif [*base_path.iterdir()] is [None]:
            print(f"Populating empty folder `{base_path.resolve()}` with {filename}")
        else:
            raise FileExistsError(
                f"The path `{base_path.resolve()}` is already occupied with something else. Consider creating new database in another folder."
            )
        # Set up readme
        README = Path(base_path, "README.md")
        README.touch()
        with README.open(mode="w") as f:
            f.writelines(
                [
                    f"# {name.title()}\n",
                    "Created using [samudra](https://github.com/samudradev/samudra)",
                    "",
                    description,
                ]
            )
    return_db = pw.SqliteDatabase(
        full_path.resolve(),
        check_same_thread=False,
    )
    return_db._state = SQLiteConnectionState()
    database_proxy.init(return_db)
    database_proxy.create_tables()
    logging.info(f"Connecting to {return_db.database}")
    append_database_list(name=name, path=full_path, engine="sqlite")
    return return_db
