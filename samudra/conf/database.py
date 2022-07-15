from contextvars import ContextVar
import logging
import os
from dataclasses import dataclass

import peewee as pw

# TODO Refactor these to depend on conf.toml
ENGINE = 'sqlite'


def get_database_connection(engine: str) -> pw.Database:
    """
    Returns the connection class based on the engine.
    """
    if engine == "sqlite":
        # Defaults to make it async-compatible (according to FastAPI/Pydantic)
        db_state_default = {"closed": None, "conn": None, "ctx": None, "transactions": None}
        db_state = ContextVar("db_state", default=db_state_default.copy())

        class PeeweeConnectionState(pw._ConnectionState):
            def __init__(self, **kwargs):
                super().__setattr__("_state", db_state)
                super().__init__(**kwargs)

            def __setattr__(self, name, value):
                self._state.get()[name] = value

            def __getattr__(self, name):
                return self._state.get()[name]

        # The DB connection object
        return_db = pw.SqliteDatabase(os.path.join(os.getcwd(), 'data', "samudra.db"))
        return_db._state = PeeweeConnectionState()

        logging.debug(f'Connection to {return_db}')
    else:
        raise NotImplementedError("Invalid engine")
    return return_db


Database = dict(
    connection=get_database_connection(engine=ENGINE)
)
