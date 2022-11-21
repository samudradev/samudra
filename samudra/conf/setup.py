import os

import peewee
import pytomlpp as toml

from samudra.conf import get_database
from samudra.conf.database.options import DatabaseEngine

settings = toml.load("conf.toml")


def access_database(local: bool = True, name: str = None) -> peewee.Database:
    if local:
        return get_database(db_name=name, engine=DatabaseEngine.SQLite, new=False)
    else:
        raise NotImplementedError("Only loca database is implemented")
