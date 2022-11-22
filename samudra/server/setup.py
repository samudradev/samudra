import logging

import peewee as pw

from samudra.models import create_tables
from samudra.conf import get_database
from samudra.conf.database.options import DatabaseEngine
from conf.setup import settings

# TODO Remove ENGINE config
ENGINE = settings.get("database").get("engine", None)
DATABASE_NAME = settings.get("database").get("name", "samudra")
PATH = ''

SERVER_DATABASE: pw.Database = get_database(engine=DatabaseEngine[ENGINE], db_name=DATABASE_NAME, path=PATH, new=True)
create_tables(database=SERVER_DATABASE)