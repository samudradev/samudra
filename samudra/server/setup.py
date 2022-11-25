import logging

import peewee as pw

from samudra.models import create_tables
from samudra.conf import get_database
from samudra.conf.database.options import DatabaseEngine
from conf.setup import settings

# TODO Remove ENGINE config
ENGINE = settings.get("database").get("engine", None)
DATABASE_NAME = settings.get("database").get("name", "samudra")
PATH = ""

# We should find a way to only pass `new=True` upon first initialization of the server
# But pass `new=False` when restarting the server OR when database already exists
SERVER_DATABASE: pw.Database = get_database(
    engine=DatabaseEngine[ENGINE], db_name=DATABASE_NAME, path=PATH, new=False
)
create_tables(database=SERVER_DATABASE)
