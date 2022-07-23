import datetime
from typing import Optional

import pydantic as pyd

from samudra import models
from samudra.schemas._helper import PeeweeGetterDict


class CakupanBase(pyd.BaseModel):
    nama: str
    keterangan: Optional[str]

    model: models.BaseTable = models.Cakupan


class CakupanResponse(CakupanBase):
    # --- Record specific fields
    id: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
