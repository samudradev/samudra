from typing import List

import pydantic as pyd

from samudra.schemas.tables._helper import PeeweeGetterDict, ORMSchema
from samudra.schemas.tables.konsep import KonsepResponseFromTables


class Token(pyd.BaseModel):
    access_token: str
    token_type: str


class LogMasukResponse(ORMSchema):
    pengguna: str
    token: Token


class DaftarResponse(ORMSchema):
    pengguna: str
    mesej: str
