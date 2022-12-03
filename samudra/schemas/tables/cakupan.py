from typing import Optional

from samudra.schemas.tables._helper import ORMSchema


class CakupanResponse(ORMSchema):
    # --- Record specific fields
    nama: str
    keterangan: Optional[str]


class AttachCakupanToResponse(ORMSchema):
    cakupan: CakupanResponse
