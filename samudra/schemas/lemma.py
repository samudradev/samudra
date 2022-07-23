import datetime
from typing import List

import pydantic as pyd

from samudra import models
from samudra.schemas._helper import PeeweeGetterDict
from samudra.schemas.konsep import KonsepResponse


class LemmaBase(pyd.BaseModel):
    nama: str
    model: models.BaseTable = models.Lemma


class LemmaResponse(LemmaBase):
    id: int
    # --- Relationships
    konsep: List[KonsepResponse]

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
