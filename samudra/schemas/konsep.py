import datetime
from typing import Optional, List, Any

import pydantic as pyd

from samudra import models
from samudra.schemas._helper import PeeweeGetterDict
from samudra.schemas.cakupan import CakupanRecord, CakupanCreation
from samudra.schemas.kata_asing import KataAsingRecord, KataAsingCreation


class KonsepBase(pyd.BaseModel):
    golongan: str
    keterangan: str
    tertib: Optional[int]

    model: models.BaseTable = models.Konsep


class KonsepCreation(KonsepBase):
    # --- Relationships
    cakupan: Optional[List[CakupanCreation]]
    kata_asing: Optional[List[KataAsingCreation]]
    lemma: Any


class KonsepRecord(KonsepBase):
    # --- Record specific fields
    id: int
    tarikh_masuk: datetime.datetime
    # --- Avoid circular dependencies
    lemma: str
    # --- Relationships
    cakupan: Optional[List[CakupanRecord]]
    kata_asing: Optional[List[KataAsingRecord]]

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
