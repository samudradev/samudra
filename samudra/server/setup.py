import logging

import peewee as pw

from samudra import models
from samudra.conf import get_database
from samudra.conf.database.core import ENGINE
from samudra.conf.database.options import DatabaseEngine

# TODO Remove ENGINE config
SERVER_DATABASE: pw.Database = get_database(engine=DatabaseEngine[ENGINE])


def check_tables(create_tables: bool = False) -> None:
    """Checks whether the tables exist or not

    Args:
        create_tables (bool, optional): Option to create tables if not exist. Defaults to False.

    Raises:
        pw.DatabaseError: Raises Database does not exist if `create_tables` is False.

    Returns:
        None: None
    """
    for TABLE in models.TABLES:
        if SERVER_DATABASE.table_exists(TABLE):
            logging.debug(f"{TABLE.__name__} existed in {SERVER_DATABASE.database}")
        else:
            if not create_tables:
                raise pw.DatabaseError(
                    f"{TABLE.__name__} not existed in {SERVER_DATABASE.database}"
                )
    if create_tables:
        SERVER_DATABASE.create_tables([*models.TABLES, *models.JOIN_TABLES], safe=True)
    return None


def drop_tables() -> None:
    """Drop all tables to start a new server from scratch"""
    SERVER_DATABASE.drop_tables([*models.TABLES, *models.JOIN_TABLES])
    logging.info("TABLES DROPPED")
