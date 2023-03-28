from typing import List

from samudra.schemas.tables._helper import ORMSchema
from samudra.schemas.tables.konsep import KonsepResponseFromTables


class LemmaResponse(ORMSchema):
    id: int
    nama: str
    # --- Relationships
    konsep: List[KonsepResponseFromTables]
