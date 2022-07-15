import datetime

import pydantic as pyd

from samudra.models.perwakilan_moden import JenisPerwakilanModen


class JenisPerwakilanModenBase(pyd.BaseModel):
    keterangan: str


class JenisPerwakilanModenCreation(JenisPerwakilanModenBase):
    pass


class JenisPerwakilanModenRecord(JenisPerwakilanModenBase):
    # --- Record specific field
    id: int
    tarikh_masuk: datetime.datetime

    class Config:
        orm_mode = True


class PerwakilanModenBase(pyd.Base):
    keterangan: str


class PerwakilanModenCreation(PerwakilanModenBase):
    pass


class PerwakilanModenRecord(PerwakilanModenBase):
    # --- Record specific field
    id: int
    tarikh_masuk: datetime.datetime
    # --- Relationships
    jenis: JenisPerwakilanModenRecord

    class Config:
        orm_mode = True
