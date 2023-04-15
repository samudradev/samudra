from typing import Any, List, Optional

import peewee
from pydantic import BaseModel
from pydantic.utils import GetterDict


class _PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


class FromPeeweeDatabase(BaseModel):
    class Config:
        orm_mode = True
        getter_dict = _PeeweeGetterDict


class GolonganKataData(FromPeeweeDatabase):
    id: str
    nama: str
    keterangan: str


class CakupanData(FromPeeweeDatabase):
    id: int
    nama: str
    keterangan: Optional[str]


class KonsepToCakupanConnector(FromPeeweeDatabase):
    cakupan: CakupanData


class KataAsingData(FromPeeweeDatabase):
    id: int
    nama: str
    bahasa: str


class KonsepToKataAsingConnector(FromPeeweeDatabase):
    kata_asing: KataAsingData


class KonsepData(FromPeeweeDatabase):
    id: int
    golongan: GolonganKataData
    keterangan: str
    tertib: Optional[int]
    cakupan: List[Optional[KonsepToCakupanConnector]]
    kata_asing: List[Optional[KataAsingData]]


class LemmaData(FromPeeweeDatabase):
    id: int
    nama: str
    konsep: List[KonsepData]
