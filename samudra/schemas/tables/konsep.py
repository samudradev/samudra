from typing import Optional, List

import pydantic as pyd

from samudra import models
from samudra.schemas.tables._helper import PeeweeGetterDict, ORMSchema
from samudra.schemas.tables.cakupan import AttachCakupanToResponse, CakupanResponse
from samudra.schemas.tables.kata_asing import (
    AttachKataAsingToResponse,
    KataAsingResponse,
)


class KonsepResponseFromAnnotatedBody(ORMSchema):
    id: int
    golongan: str
    keterangan: str
    tertib: Optional[int]
    # --- Relationships
    cakupan: Optional[List[CakupanResponse]]
    kata_asing: Optional[List[KataAsingResponse]]


class KonsepResponseFromTables(ORMSchema):
    id: int
    golongan: str
    keterangan: str
    tertib: Optional[int]
    # --- Relationships
    cakupan: Optional[List[AttachCakupanToResponse]]
    kata_asing: Optional[List[AttachKataAsingToResponse]]
