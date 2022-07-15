import datetime
from typing import List

import pydantic as pyd

from samudra import models
from samudra.schemas.konsep import KonsepRecord, KonsepCreation


class LemmaBase(pyd.BaseModel):
    nama: str
    model: models.BaseTable = models.Lemma


class LemmaCreation(LemmaBase):
    # --- Relationships
    konsep: List[KonsepCreation]


class LemmaRecord(LemmaCreation):
    # --- Record specific fields
    id: int
    tarikh_masuk: datetime.datetime
    # --- Relationships
    konsep: List[KonsepRecord]

    class Config:
        orm_mode = True
