from typing import List

from fastapi import FastAPI, Depends, HTTPException
from samudra import models, schemas
from samudra.tools.setup import get_db
from samudra.tools import crud

from main import app


@app.get("/lemmas/", response_model=None, dependencies=[Depends(get_db)])
def get_all_lemma(limit: int = None) -> List[models.Lemma]:
    return crud.get_all_lemma(limit=limit)


@app.get("/lemma/id/{_id}", response_model=schemas.LemmaRecord, dependencies=[Depends(get_db)])
def get_lemma_by_id(_id: int) -> List[models.Lemma]:
    return crud.get_lemma_by_id(lemma_id=_id)


@app.get("/lemma/{nama}", response_model=schemas.LemmaRecord, dependencies=[Depends(get_db)])
def read_lemma(nama: str) -> List[models.Lemma]:
    db_lemma = crud.get_lemma_by_name(nama=nama)
    if db_lemma is None:
        raise HTTPException(status_code=404, detail='Lemma not in record')
    return db_lemma
