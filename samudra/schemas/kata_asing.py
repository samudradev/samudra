import datetime

import pydantic as pyd

from samudra import models
from samudra.schemas._helper import PeeweeGetterDict


class KataAsingBase(pyd.BaseModel):
    nama: str
    bahasa: str

    model: models.BaseTable = models.KataAsing


class KataAsingResponse(KataAsingBase):
    # --- Record specific fields
    id: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
