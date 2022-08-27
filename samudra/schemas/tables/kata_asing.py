from typing import Optional

from samudra.schemas.tables._helper import ORMSchema


class KataAsingResponse(ORMSchema):
    # --- Record specific fields
    nama: Optional[str]
    bahasa: Optional[str]


class AttachKataAsingToResponse(ORMSchema):
    kata_asing: KataAsingResponse
