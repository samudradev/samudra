from typing import List

import pydantic as pyd

from samudra.schemas.tables._helper import PeeweeGetterDict, ORMSchema
from samudra.schemas.tables.konsep import KonsepResponseFromTables


class LemmaResponse(ORMSchema):
    id: int
    nama: str
    # --- Relationships
    konsep: List[KonsepResponseFromTables]
