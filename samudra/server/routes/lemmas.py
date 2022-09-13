from typing import List, Union, Dict, Optional

import pydantic
from fastapi import APIRouter, Depends, HTTPException, Query

from samudra import models, schemas
from samudra.core import crud
from samudra.server.dependencies import get_db
from schemas.input.query_filter import QueryFilter
from server.dependencies import oauth2_scheme

router = APIRouter(prefix="/lemma", dependencies=[Depends(get_db)])


@router.get("/", response_model=List[schemas.LemmaResponse])
def get_all_lemma(
    limit: Optional[int] = Query(default=None),
    cakupan: Optional[List[str]] = Query(default=None),
    kata_asing: Optional[List[str]] = Query(default=None),
) -> List[models.Lemma]:
    return crud.get_lemma(
        QueryFilter(limit=limit, cakupan=cakupan, kata_asing=kata_asing)
    )


@router.get("/{nama}", response_model=List[schemas.LemmaResponse])
def read_lemma(
    nama: str,
    limit: Optional[int] = Query(default=None),
    cakupan: Optional[List[str]] = Query(default=None),
    kata_asing: Optional[List[str]] = Query(default=None),
) -> List[models.Lemma]:
    db_lemma = crud.get_lemma_by_name(
        nama=nama,
        query=QueryFilter(limit=limit, cakupan=cakupan, kata_asing=kata_asing),
    )
    if db_lemma is None:
        raise HTTPException(status_code=404, detail="Lemma not in record")
    return db_lemma


@router.post("/{nama}", response_model=schemas.KonsepResponseFromAnnotatedBody)
def create_lemma(
    nama: str, post: schemas.AnnotatedText, token: str = Depends(oauth2_scheme)
) -> Union[models.Konsep, schemas.AnnotatedText]:
    try:
        to_return = crud.create_konsep(post, lemma_name=nama)
    except SyntaxError as e:
        raise HTTPException(status_code=400, detail=e.msg)
    return to_return


@router.delete("/id/{_id}", response_model=Dict[str, int])
def delete_lemma(_id: int, token: str = Depends(oauth2_scheme)) -> Dict[str, int]:
    lemma = crud.get_lemma_by_id(_id)[0]
    return {"deleted": crud.delete_lemma(lemma)}
