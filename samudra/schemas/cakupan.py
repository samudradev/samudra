import datetime

import pydantic as pyd


class CakupanBase(pyd.BaseModel):
    nama: str
    keterangan: str


class CakupanCreation(CakupanBase):
    pass


class CakupanRecord(CakupanBase):
    # --- Record specific fields
    id: int
    tarikh_masuk: datetime.datetime

    class Config:
        orm_mode = True
