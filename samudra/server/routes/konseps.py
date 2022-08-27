from typing import List, Union, Optional, Dict, Any

import pydantic
from fastapi import APIRouter, Depends, HTTPException

from samudra import models, schemas
from samudra.core import crud
from samudra.server.dependencies import get_db

router = APIRouter(prefix="/konsep", dependencies=[Depends(get_db)])


@router.get("/", response_model=List[schemas.KonsepResponseFromTables])
def get_all_konsep(limit: Optional[int] = None) -> List[models.Konsep]:
    return crud.get_konsep_minimum_info(where=None, limit=limit)
