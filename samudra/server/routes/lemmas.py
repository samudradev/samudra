from typing import List, Union, Optional, Dict

import pydantic
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from samudra import models, schemas
from samudra.core import crud
from samudra.server.dependencies import get_db

router = APIRouter(
    prefix="/lemma",
    dependencies=[Depends(get_db)]
)


# TODO: Add security!
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/", response_model=List[schemas.LemmaResponse])
def get_all_lemma(limit: int = None, token: str = Depends(oauth2_scheme)) -> List[models.Lemma]:
    return crud.get_lemma(limit=limit)


@router.get("/{nama}", response_model=List[schemas.LemmaResponse])
def read_lemma(nama: str, token: str = Depends(oauth2_scheme)) -> List[models.Lemma]:
    db_lemma = crud.get_lemma_by_name(nama=nama)
    if db_lemma is None:
        raise HTTPException(status_code=404, detail='Lemma not in record')
    return db_lemma


@router.post('/{nama}', response_model=schemas.KonsepResponseFromAnnotatedBody)
def create_lemma(nama: str, post: schemas.AnnotatedText, token: str = Depends(oauth2_scheme)) -> Union[models.Konsep, schemas.AnnotatedText]:
    try:
        to_return = crud.create_konsep(post, lemma_name=nama)
    except SyntaxError as e:
        raise HTTPException(status_code=400, detail=e.msg)
    try:
        return to_return
    except pydantic.ValidationError:
        raise HTTPException(status_code=400, detail=post.dict())


@router.get("/id/{_id}", response_model=List[schemas.LemmaResponse])
def get_lemma_by_id(_id: int, token: str = Depends(oauth2_scheme)) -> List[models.Lemma]:
    return crud.get_lemma_by_id(lemma_id=_id)


@router.delete('/id/{_id}', response_model=Dict[str, int])
def delete_lemma(_id: int, token: str = Depends(oauth2_scheme)) -> Dict[str, int]:
    lemma = crud.get_lemma_by_id(_id)[0]
    return {"deleted": crud.delete_lemma(lemma)}
