import logging

import peewee as pw
import uvicorn
from fastapi import FastAPI

from samudra import models
from samudra.conf import Database

app = FastAPI()


def check_tables(create_tables: bool = False) -> None:
    for TABLE in models.TABLES:
        if Database.connection.table_exists(TABLE):
            logging.debug(f"{TABLE.__name__} existed in {Database.connection.database}")
        else:
            if not create_tables:
                raise pw.DatabaseError(f"{TABLE.__name__} not existed in {Database.connection.database}")
    if create_tables:
        Database.connection.create_tables(models.TABLES)
    return None


if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, reload=True)
