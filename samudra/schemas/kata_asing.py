import datetime

import pydantic as pyd

from samudra import models


class KataAsingBase(pyd.BaseModel):
    lemma: str
    golongan: str

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
