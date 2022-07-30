from typing import Optional

import pydantic as pyd

from samudra import models
from samudra.models import kata_asing
from samudra.schemas.tables._helper import PeeweeGetterDict, ORMSchema


class KataAsingResponse(ORMSchema):
    # --- Record specific fields
    nama: Optional[str]
    bahasa: Optional[str]


class AttachKataAsingToResponse(ORMSchema):
    kata_asing: KataAsingResponse
