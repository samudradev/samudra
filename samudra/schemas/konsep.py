import datetime
from typing import Optional, List

import pydantic as pyd

from samudra.schemas.cakupan import CakupanRecord, CakupanCreation
from samudra.schemas.kata_asing import KataAsingRecord, KataAsingCreation
from samudra.schemas.perwakilan_moden import PerwakilanModenRecord, PerwakilanModenCreation


class KonsepBase(pyd.BaseModel):
    golongan: str
    keterangan: str
    tertib: Optional[int]


class KonsepCreation(KonsepBase):
    # --- Relationships
    cakupan: Optional[List[CakupanCreation]]
    kata_asing: Optional[List[KataAsingCreation]]
    perwakilan_moden: Optional[List[PerwakilanModenCreation]]


class KonsepRecord(KonsepBase):
    # --- Record specific fields
    id: int
    tarikh_masuk: datetime.datetime
    # --- Avoid circular dependencies
    lemma: str
    # --- Relationships
    cakupan: Optional[List[CakupanRecord]]
    kata_asing: Optional[List[KataAsingRecord]]
    perwakilan_moden: Optional[List[PerwakilanModenRecord]]

    class Config:
        orm_mode = True
