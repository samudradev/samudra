from typing import List, Union, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from samudra import models, schemas
from samudra.core import crud
from samudra.server.dependencies import get_db
from samudra.schemas.input.query_filter import QueryFilter
from samudra.server.dependencies import oauth2_scheme

router = APIRouter(prefix="/lemma", dependencies=[Depends(get_db)])


@router.get("/", response_model=List[schemas.LemmaResponse])
def get_all_lemma(
    limit: Optional[int] = Query(default=None),
    cakupan: Optional[List[str]] = Query(default=None),
    kata_asing: Optional[List[str]] = Query(default=None),
) -> List[models.Lemma]:
    """GET `/lemma/`. Queries all lemma within the defined query parameters.

    Args:
        limit (Optional[int], optional): Limit number of hits. Defaults to Query(default=None).
        cakupan (Optional[List[str]], optional): Context of meaning. Defaults to Query(default=None).
        kata_asing (Optional[List[str]], optional): Containing these foreign words. Defaults to Query(default=None).

    Returns:
        List[models.Lemma]: List of Lemma and its meaning.
    """
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
    """GET `/lemma/{nama}`. Queries the database for lemma with value `nama={nama}`.

    Args:
        nama (str): the dictionary entry
        limit (Optional[int], optional): Limit number of hits. Defaults to Query(default=None).
        cakupan (Optional[List[str]], optional): Context of meaning. Defaults to Query(default=None).
        kata_asing (Optional[List[str]], optional): Containing these foreign words. Defaults to Query(default=None).

    Raises:
        HTTPException: 404 Exception if no lemma found in record

    Returns:
        List[models.Lemma]: List of Lemma and its meaning.
    """
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
    """POST `/lemma/{nama}`. Inserts the lemma with value `nama={nama}` and `post` into the database.

    !!! important "PROTECTED"
        user `token` required

    Args:
        nama (str): the dictionary entry
        post (schemas.AnnotatedText): An annotated text containing meaning, context, and foreign words.

    Raises:
        HTTPException: 400 Bad Query Exception if it has bad AnnotatedText.

    Returns:
        If successful: [`Konsep`][samudra.models.core.konsep.Konsep]. If unsuccessful: [`schemas.AnnotatedText`][samudra.schemas.input.annotated_text.AnnotatedText] for helpful error messages.
    """
    try:
        to_return = crud.create_konsep_by_annotated_text(post, lemma_name=nama)
    except SyntaxError as e:
        raise HTTPException(status_code=400, detail=e.msg)
    return to_return


@router.delete("/id/{_id}", response_model=Dict[str, int])
def delete_lemma(_id: int, token: str = Depends(oauth2_scheme)) -> Dict[str, int]:
    """DELETE `/lemma/id/{_id}`. Deletes lemma with value `id={_id}`

    !!! important "PROTECTED"
        user `token` required

    Args:
        _id (int): Id of lemma

    Returns:
        Returns how many items are deleted.
    """
    lemma = crud.get_lemma_by_id(_id)[0]
    return {"deleted": crud.delete_lemma(lemma)}
