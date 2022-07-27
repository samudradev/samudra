from typing import Optional, List

import pydantic as pyd

from samudra import models
from samudra.schemas.tables._helper import PeeweeGetterDict
from samudra.schemas.tables.cakupan import CakupanResponseAsAttachment
from samudra.schemas.tables.kata_asing import KataAsingResponseAsAttachment


class KonsepResponse(pyd.BaseModel):
    id: int
    golongan: str
    keterangan: str
    tertib: Optional[int]
    # --- Relationships
    cakupan: Optional[List[CakupanResponseAsAttachment]]
    kata_asing: Optional[List[KataAsingResponseAsAttachment]]

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
