from fastapi import APIRouter, Depends, HTTPException

import schemas
from core import crud
from server.dependencies import get_db, oauth2_scheme

router = APIRouter(prefix="/golongan_kata", dependencies=[Depends(get_db)])


@router.post('/new')
def create_golongan_kata(post: schemas.CreateGolonganKata, token: str = Depends(oauth2_scheme)):
    try:
        return crud.create_golongan_kata(data=post)
    except ValueError as e:
        return HTTPException(status_code=400, detail=e)
