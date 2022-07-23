import datetime
from typing import Optional, List, Any

import pydantic as pyd

from samudra import models
from samudra.schemas._helper import PeeweeGetterDict
from samudra.schemas.cakupan import CakupanResponse
from samudra.schemas.kata_asing import KataAsingResponse


class KonsepBase(pyd.BaseModel):
    golongan: str
    keterangan: str
    tertib: Optional[int]

    model: models.BaseTable = models.Konsep


class KonsepResponse(KonsepBase):
    # --- Record specific fields
    id: int
    # --- Relationships
    cakupan: Optional[List[CakupanResponse]]
    kata_asing: Optional[List[KataAsingResponse]]

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
