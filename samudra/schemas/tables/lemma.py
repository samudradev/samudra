from typing import List

import pydantic as pyd

from samudra.schemas.tables._helper import PeeweeGetterDict
from samudra.schemas.tables.konsep import KonsepResponse


class LemmaResponse(pyd.BaseModel):
    id: int
    nama: str
    # --- Relationships
    konsep: List[KonsepResponse]

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
