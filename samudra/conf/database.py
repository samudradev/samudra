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
        return_value = pw.SqliteDatabase(os.path.join(os.getcwd(), 'data', "samudra.db"))
        logging.debug(f'Connection to {return_value}')
        return return_value
    else:
        raise NotImplementedError("Invalid engine")


Database = dict(
    connection=get_database_connection(engine=ENGINE)
)
