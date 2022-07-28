from typing import List, Union, Optional, Dict

import pydantic
from fastapi import APIRouter, Depends, HTTPException

from samudra import models, schemas
from samudra.core import crud
from samudra.server.dependencies import get_db

router = APIRouter(
    prefix="/lemmas",
    dependencies=[Depends(get_db)]
)


# TODO: Add security!

@router.get("/lemmas/", response_model=List[schemas.LemmaResponse])
def get_all_lemma(limit: int = None) -> List[models.Lemma]:
    return crud.get_all_lemma(limit=limit)


@router.get("/lemma/id/{_id}", response_model=List[schemas.LemmaResponse])
def get_lemma_by_id(_id: int) -> List[models.Lemma]:
    return crud.get_lemma_by_id(lemma_id=_id)


@router.get("/lemma/{nama}", response_model=List[schemas.LemmaResponse])
def read_lemma(nama: str) -> List[models.Lemma]:
    db_lemma = crud.get_lemma_by_name(nama=nama)
    if db_lemma is None:
        raise HTTPException(status_code=404, detail='Lemma not in record')
    return db_lemma


@router.get('/konseps/', response_model=List[schemas.KonsepResponse])
def get_all_konsep(limit: Optional[int] = None) -> List[models.Konsep]:
    return crud.get_all_konsep(limit=limit)


@router.post('/lemma/{nama}', response_model=schemas.KonsepResponse)
def create_lemma(nama: str, post: schemas.AnnotatedText) -> Union[models.Konsep, schemas.AnnotatedText]:
    try:
        to_return = crud.create_konsep(post, lemma_name=nama)
    except SyntaxError as e:
        raise HTTPException(status_code=400, detail=e.msg)
    try:
        return to_return
    except pydantic.ValidationError:
        raise HTTPException(status_code=400, detail=post.dict())


@router.delete('/lemma/{id}', response_model=Dict[str, int])
def delete_lemma(_id: int) -> Dict[str, int]:
    lemma = crud.get_lemma_by_id(_id)[0]
    return {"deleted": crud.delete_lemma(lemma)}
