from typing import Optional

import pydantic as pyd

from samudra import models
from samudra.schemas.tables._helper import PeeweeGetterDict, ORMSchema


class CakupanResponse(ORMSchema):
    # --- Record specific fields
    nama: str
    keterangan: Optional[str]


class AttachCakupanToResponse(ORMSchema):
    cakupan: CakupanResponse
