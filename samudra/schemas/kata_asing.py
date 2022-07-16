import datetime

import pydantic as pyd

from samudra import models
from samudra.schemas._helper import PeeweeGetterDict


class KataAsingBase(pyd.BaseModel):
    nama: str
    golongan: str
    bahasa: str

    model: models.BaseTable = models.KataAsing


class KataAsingCreation(KataAsingBase):
    pass


class KataAsingRecord(KataAsingBase):
    # --- Record specific fields
    id: int
    tarikh_masuk: datetime.datetime

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
