import logging
from typing import List

import peewee as pw
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from samudra import models, schemas, crud, tools
from samudra.conf import Database
from samudra.conf.database import db_state_default

app = FastAPI()
SLEEP_TIME: int = 10
CSV_FILENAME: str = 'mocks.xlsx'

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
    for TABLE in models.TABLES:
        if Database.connection.table_exists(TABLE):
            logging.debug(f"{TABLE.__name__} existed in {Database.connection.database}")
        else:
            raise pw.DatabaseError(f"{TABLE.__name__} existed in {Database.connection.database}")
    return None


if __name__ == '__main__':
    check_tables()
    tools.read_excel(CSV_FILENAME)

    # tools.csv_to_sql(CSV_FILENAME, preserve_csv_data=False)  # Inject data
    # uvicorn.run("main:app", port=8000, reload=True)
