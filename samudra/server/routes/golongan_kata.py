from typing import Union
from fastapi import APIRouter, Depends, HTTPException
from samudra import models

from samudra import schemas
from samudra.core import crud
from samudra.server.dependencies import get_db, oauth2_scheme

router = APIRouter(prefix="/golongan", dependencies=[Depends(get_db)])


@router.post("/new")
def create_golongan_kata(
    post: schemas.CreateGolonganKata, token: str = Depends(oauth2_scheme)
) -> Union[models.GolonganKata, schemas.CreateGolonganKata]:
    """CREATE `/golongan/new/`. Creates word class with value defined in `post`.

    !!! important "PROTECTED"
        user `token` required.

    Args:
        post (schemas.CreateGolonganKata): A JSON Object to define [`models.GolonganKata`][samudra.models.core.konsep.GolonganKata]

    Returns:
        If successful: [`GolonganKata`][samudra.models.core.konsep.GolonganKata]. If unsuccessful: [`schemas.CreateGolonganKata`][samudra.schemas.input.annotated_text.CreateGolonganKata] for helpful error messages.
    """
    try:
        return crud.create_golongan_kata(data=post)
    except ValueError as e:
        return HTTPException(status_code=400, detail=e)
