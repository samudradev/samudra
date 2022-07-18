import datetime
from typing import Optional

import pydantic as pyd

from samudra import models
from samudra.schemas._helper import PeeweeGetterDict


class CakupanBase(pyd.BaseModel):
    nama: str
    keterangan: Optional[str]

    model: models.BaseTable = models.Cakupan


class CakupanCreation(CakupanBase):
    pass


class CakupanRecord(CakupanBase):
    # --- Record specific fields
    id: int
    tarikh_masuk: datetime.datetime

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
