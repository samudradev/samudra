from typing import List

import pydantic as pyd

from samudra.schemas.tables._helper import PeeweeGetterDict, ORMSchema
from samudra.schemas.tables.konsep import KonsepResponseFromTables


class Token(pyd.BaseModel):
    """Token"""

    access_token: str
    token_type: str


class LogMasukResponse(ORMSchema):
    """LogMasukResponse"""

    pengguna: str
    token: Token


class DaftarResponse(ORMSchema):
    """DaftarResponse"""

    pengguna: str
    mesej: str
