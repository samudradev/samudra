import datetime

import pydantic as pyd

from samudra import models


class CakupanBase(pyd.BaseModel):
    nama: str
    keterangan: str

    model: models.BaseTable = models.Cakupan


class CakupanCreation(CakupanBase):
    pass


class CakupanRecord(CakupanBase):
    # --- Record specific fields
    id: int
    tarikh_masuk: datetime.datetime

    class Config:
        orm_mode = True
