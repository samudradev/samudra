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
        retrun_value = pw.SqliteDatabase(path:=os.path.join(os.getcwd(), 'data', "samudra.db"))
        print(path)
        return retrun_value
    else:
        raise NotImplementedError("Invalid engine")


Database = dict(
    connection=get_database_connection(engine=ENGINE)
)

