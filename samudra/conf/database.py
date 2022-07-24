from contextvars import ContextVar
import logging
import os
from dataclasses import dataclass

import peewee as pw
from dotenv import load_dotenv

load_dotenv()

# TODO Refactor these to depend on conf.toml
ENGINE = os.getenv('ENGINE')
DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PORT = os.getenv('DATABASE_PORT')
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

db_state_default = {"closed": None, "conn": None, "ctx": None, "transactions": None}
db_state = ContextVar("db_state", default=db_state_default.copy())


def get_database_connection(engine: str) -> pw.Database:
    """
    Returns the connection class based on the engine.
    """
    if engine == "sqlite":
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
        return_db = pw.SqliteDatabase(os.path.join(os.getcwd(), 'data', f"{DATABASE_NAME}.db"))
        return_db._state = PeeweeConnectionState()

        logging.debug(f'Connecting to to {return_db.database}')
    elif engine == 'mysql':
        return_db = pw.MySQLDatabase(DATABASE_NAME, host=DATABASE_HOST, port=DATABASE_PORT, user=USERNAME,
                                     password=PASSWORD)
    else:
        raise NotImplementedError("Invalid engine")
    return return_db


@dataclass
class Database:
    connection = get_database_connection(engine=ENGINE)
