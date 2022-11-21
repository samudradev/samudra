from contextvars import ContextVar
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from unicodedata import name

import peewee as pw

from conf.local import get_database_info

# ! Importing settings will create circular import
# from conf.setup import settings
from samudra.conf.database.options import DatabaseEngine

# TODO: Enforce requirements per database engine


# As settings
# ENGINE = settings.get("database").get("engine", None)
# DATABASE_NAME = settings.get("database").get("name", "samudra")

db_state_default = {"closed": None, "conn": None, "ctx": None, "transactions": None}
db_state = ContextVar("db_state", default=db_state_default.copy())


def get_database(db_name: str, engine: DatabaseEngine, **kwargs) -> pw.Database:
    """
    Returns the connection class based on the engine.
    """
    if engine is None or engine not in DatabaseEngine.__members__.values():
        raise ValueError(
            "Please specify database engine in conf.toml. You entered {}. Valid values are: \n - {}".format(
                engine, "\n - ".join(DatabaseEngine.__members__.values())
            )
        )
    if engine == DatabaseEngine.SQLite:
        return get_sqlite(
            folder=db_name, path=kwargs.pop("path"), new=kwargs.pop("new"), **kwargs
        )

    DATABASE_HOST = os.getenv("DATABASE_HOST")
    DATABASE_PORT = int(os.getenv("DATABASE_PORT"))
    DATABASE_OPTIONS = os.getenv("DATABASE_OPTIONS")
    USERNAME = os.getenv("DATABASE_USERNAME")
    PASSWORD = os.getenv("DATABASE_PASSWORD")
    SSL_MODE = os.getenv("SSL_MODE")

    if engine == DatabaseEngine.MySQL:
        conn_str = f"mysql://{USERNAME}:{PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{db_name}?ssl-mode=REQUIRED"
        return_db = pw.MySQLDatabase(conn_str)
        logging.info(f"Connecting to {return_db.database} as {USERNAME}")
    if engine == DatabaseEngine.CockroachDB:
        from playhouse.cockroachdb import CockroachDatabase

        conn_str = f"postgresql://{USERNAME}:{PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{db_name}?sslmode=verify-full&options={DATABASE_OPTIONS}"
        return_db = CockroachDatabase(conn_str)
        logging.info(f"Connecting to {return_db.database} as {USERNAME}")
    else:
        raise NotImplementedError("Invalid engine")
    return return_db


def get_sqlite(folder: str, path: str, db_file: str = "samudra.db", new: bool = False):
    # Defaults to make it async-compatible (according to FastAPI/Pydantic)
    class PeeweeConnectionState(pw._ConnectionState):
        def __init__(self, **kwargs):
            super().__setattr__("_state", db_state)
            super().__init__(**kwargs)

        def __setattr__(self, name, value):
            self._state.get()[name] = value

        def __getattr__(self, name):
            return self._state.get()[name]

    # The DB connection object
    # ? Perlu ke test?
    # TODO Add Test
    if new:
        base_path: Path = Path(path, folder)
        full_path: Path = Path(base_path, db_file)
        try:
            base_path.mkdir(parents=True)
        except FileExistsError:
            if full_path in [*base_path.iterdir()]:
                raise FileExistsError(
                    f"A samudra database already exists in {full_path.resolve()}"
                )
            elif [*base_path.iterdir()] is [None]:
                print(f"Populating empty folder `{base_path.resolve()}` with {db_file}")
            else:
                raise FileExistsError(
                    f"The path `{base_path.resolve()}` is already occupied with something else. Consider using other folder."
                )
        # Set up readme
        README = Path(base_path, "README.md")
        README.touch()
        with README.open(mode="w") as f:
            f.writelines(
                [
                    f"# {folder.title()}\n",
                    "Created using [samudra](https://github.com/samudradev/samudra)",
                ]
            )
    else:
        db_obj = get_database_info(name=db_file)
        if db_obj is None:
            return FileNotFoundError(
                f"The database name {db_file} is not found. Perhaps it is not created yet. Pass the key `new=True` if that's the case"
            )
        base_path: Path = Path(db_obj["path"], folder=db_file)
        full_path: Path = Path(base_path, db_file)
    return_db = pw.SqliteDatabase(
        full_path.resolve(),
        check_same_thread=False,
    )
    return_db._state = PeeweeConnectionState()
    logging.info(f"Connecting to {return_db.database}")
    return return_db
