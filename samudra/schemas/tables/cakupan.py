from typing import Optional

import pydantic as pyd

from samudra import models
from samudra.schemas.tables._helper import PeeweeGetterDict


class CakupanResponseAsAttachment(pyd.BaseModel):
    # --- Record specific fields
    nama: str
    keterangan: Optional[str]

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class CakupanResponse(CakupanResponseAsAttachment):
    id: int
