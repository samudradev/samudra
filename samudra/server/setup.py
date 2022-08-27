import logging

import peewee as pw

from samudra import models
from samudra.conf import Database


def check_tables(create_tables: bool = False) -> None:
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
    Database.connection.drop_tables([*models.TABLES, *models.JOIN_TABLES])
    logging.info("TABLES DROPPED")
