import peewee
import pytomlpp as toml

from samudra.conf import get_database
from samudra.conf.database.core import get_active_database
from samudra.conf.database.options import DatabaseEngine
from samudra.models.base import database_proxy

try:
    settings = toml.load("conf.toml")
except FileNotFoundError:
    pass


def access_database(local: bool = True, name: str = None) -> peewee.Database:
    if local:
        return get_database(name=name, engine=DatabaseEngine.SQLite, new=False)
    else:
        raise NotImplementedError("Only local database is implemented")


def bind_proxy_with_active_database() -> None:
    database_proxy.initialize(get_active_database())
