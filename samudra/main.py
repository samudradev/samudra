import logging

import peewee as pw
import pydantic
import uvicorn

from typing import List, Union, Optional

from fastapi import Depends, FastAPI, HTTPException
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from samudra import models, schemas
from samudra.core import crud
from samudra.conf import Database
from samudra.conf.database.core import db_state_default

app = FastAPI()

SLEEP_TIME: int = 500_000

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
    try:
        Database.connection._state._state.set(db_state_default.copy())
        Database.connection._state.reset()
    except AttributeError:
        pass


def get_db(db_state=Depends(reset_db_state)):
    try:
        Database.connection.connect()
        yield
    finally:
        if not Database.connection.is_closed():
            Database.connection.close()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"OMG! The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)


@app.get("/lemmas/", response_model=List[schemas.LemmaResponse], dependencies=[Depends(get_db)])
def get_all_lemma(limit: int = None) -> List[models.Lemma]:
    return crud.get_all_lemma(limit=limit)


@app.get("/lemma/id/{_id}", response_model=List[schemas.LemmaResponse], dependencies=[Depends(get_db)])
def get_lemma_by_id(_id: int) -> List[models.Lemma]:
    return crud.get_lemma_by_id(lemma_id=_id)


@app.get("/lemma/{nama}", response_model=List[schemas.LemmaResponse], dependencies=[Depends(get_db)])
def read_lemma(nama: str) -> List[models.Lemma]:
    db_lemma = crud.get_lemma_by_name(nama=nama)
    if db_lemma is None:
        raise HTTPException(status_code=404, detail='Lemma not in record')
    return db_lemma


@app.get('/konseps/', response_model=List[schemas.KonsepResponse], dependencies=[Depends(get_db)])
def get_all_konsep(limit: Optional[int] = None) -> List[models.Konsep]:
    return crud.get_all_konsep(limit=limit)


@app.post('/lemma/{nama}', response_model=schemas.KonsepResponse, dependencies=[Depends(get_db)])
def create_lemma(nama: str, post: schemas.AnnotatedText) -> Union[models.Konsep, schemas.AnnotatedText]:
    try:
        to_return = crud.create_konsep(post, lemma_name=nama)
    except SyntaxError as e:
        raise HTTPException(status_code=400, detail=e.msg)
    try:
        return to_return
    except pydantic.ValidationError:
        raise HTTPException(status_code=400, detail=post.dict())


@app.delete('/lemma/{id}', response_model=int, dependencies=[Depends(get_db)])
def delete_lemma(id: int) -> int:
    lemma = crud.get_lemma_by_id(id)[0]
    return crud.delete_lemma(lemma)


def check_tables(create_tables: bool = False) -> None:
    for TABLE in models.TABLES:
        if Database.connection.table_exists(TABLE):
            logging.debug(f"{TABLE.__name__} existed in {Database.connection.database}")
        else:
            if not create_tables:
                raise pw.DatabaseError(f"{TABLE.__name__} not existed in {Database.connection.database}")
    if create_tables:
        Database.connection.create_tables([*models.TABLES, *models.JOIN_TABLES], safe=True)
    return None


def drop_tables() -> None:
    Database.connection.drop_tables([*models.TABLES, *models.JOIN_TABLES])
    logging.debug("TABLES DROPPED")


if __name__ == '__main__':
    # drop_tables()
    check_tables(create_tables=True)
    uvicorn.run("main:app", port=8000, reload=True)
