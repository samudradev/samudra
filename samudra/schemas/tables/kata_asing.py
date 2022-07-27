from typing import Optional

import pydantic as pyd

from samudra import models
from samudra.schemas.tables._helper import PeeweeGetterDict


class KataAsingResponseAsAttachment(pyd.BaseModel):
    # --- Record specific fields
    nama: Optional[str]
    bahasa: Optional[str]

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
