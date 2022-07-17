import logging
from typing import List

import peewee as pw
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from samudra import models, schemas, crud
from samudra.conf import Database
from samudra.conf.database import db_state_default
from tests import mocks

app = FastAPI()
SLEEP_TIME: int = 10

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


async def reset_db_state() -> None:
    Database.connection._state._state.set(db_state_default.copy())
    Database.connection._state.reset()


def get_db(db_state=Depends(reset_db_state)):
    try:
        Database.connection.connect()
        yield
    finally:
        if not Database.connection.is_closed():
            Database.connection.close()


# @app.post("/lemma/", response_model=schemas.LemmaRecord, dependencies=[Depends(get_db)])
# def create_lemma(lemma: schemas.LemmaCreation) -> models.Lemma:
#     db_lemma = crud.get_lemma(nama=lemma.nama)
#     if db_lemma:
#         pass
#     return crud.create_lemma(lemma=lemma)


@app.get("/lemmas/", response_model=None, dependencies=[Depends(get_db)])
def get_all_lemma() -> List[models.Lemma]:
    return crud.get_all_lemma()


@app.get("/lemma/{nama}", response_model=schemas.LemmaRecord, dependencies=[Depends(get_db)])
def read_lemma(nama: str) -> models.Lemma:
    db_lemma = crud.get_lemma(nama=nama)
    if db_lemma is None:
        raise HTTPException(status_code=404, detail='Lemma not in record')
    return db_lemma


def check_tables() -> None:
    try:
        Database.connection.connect()
        new = models.Lemma(nama='test')
        new.save()
        new.delete()
        logging.debug(f"{models.Lemma.__name__} existed in {Database.connection.database}")
    except pw.OperationalError:
        Database.connection.create_tables(models.TABLES, safe=True)
        logging.debug(f"Created {models.TABLES} in {Database.connection.name}")
    finally:
        Database.connection.close()
    return None


if __name__ == '__main__':
    check_tables()
    mock_lemma = mocks.single_complete_test_lemma()
    crud.create_lemma(mock_lemma)
    uvicorn.run("main:app", port=8000, reload=True)
