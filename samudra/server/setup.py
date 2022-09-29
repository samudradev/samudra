import logging

import peewee as pw

from samudra import models
from samudra.conf import Database


# TODO Refactor Database.connection to decouple dependency on conf


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
        if Database.connection.table_exists(TABLE):
            logging.debug(f"{TABLE.__name__} existed in {Database.connection.database}")
        else:
            if not create_tables:
                raise pw.DatabaseError(
                    f"{TABLE.__name__} not existed in {Database.connection.database}"
                )
    if create_tables:
        Database.connection.create_tables(
            [*models.TABLES, *models.JOIN_TABLES], safe=True
        )
    return None


def drop_tables() -> None:
    """Drop all tables to start a new server from scratch"""
    Database.connection.drop_tables([*models.TABLES, *models.JOIN_TABLES])
    logging.info("TABLES DROPPED")
