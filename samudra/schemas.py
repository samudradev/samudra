"""## Schema of a Lemma

If we look at [LemmaData][samudra.schemas.LemmaData] as a single JSON object, it looks like this:

```json
lemma: {
    id: int 
    nama: str
    konsep: [
        {
            id: int
            keterangan: str
            tertib: *int
            golongan: {
                id: str
                nama: str
                keterangan: str
            }
            cakupan: [
                *{
                    cakupan: {
                        id: int
                        nama: str
                        keterangan: *str
                    }
                } ...
            ]
            kata_asing: [
                *{
                    kata_asing: {
                        id: int
                        nama: str
                        bahasa: str
                    }
                } ...
            ]
        } ...
    ]
}
```
where `*` at the beginning of the type represents optional values and `[{} ...]` represents a list of objects.
"""


from typing import Any, List, Optional

import peewee
from pydantic import BaseModel
from pydantic.utils import GetterDict


class _PeeweeGetterDict(GetterDict):
    """A class to convert peewee's model query into a Python object. Used by [FromPeeweeDatabase][samudra.schemas.FromPeeweeDatabase]"""

    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


class FromPeeweeDatabase(BaseModel):
    """The base class of all the schemas which enables the inheriting objects to be able to understand and validate [peewee Models][samudra.models.base.BaseDataTable]"""

    class Config:
        orm_mode = True
        getter_dict = _PeeweeGetterDict


class GolonganKataData(FromPeeweeDatabase):
    """Object and JSONable representation of [models.GolonganKata][samudra.models.core.konsep.GolonganKata]

    | keys  | value type    |
    | :---: | :---:         |
    | id    | str |
    | nama  | str |
    | keterangan | str |
    """

    id: str
    nama: str
    keterangan: str


class CakupanData(FromPeeweeDatabase):
    """Object and JSONable representation of [models.Cakupan][samudra.models.core.cakupan.Cakupan]

    | keys  | value type    |
    | :---: | :---:         |
    | id    | int |
    | nama  | str |
    | keterangan | str (optional) |
    """

    id: int
    nama: str
    keterangan: Optional[str]


class KonsepToCakupanConnector(FromPeeweeDatabase):
    """Object and JSONable representation of [models.CakupanXKonsep][samudra.models.core.cakupan.CakupanXKonsep] with the exception that it is a one way connection.

    !!! note
        The connection has to be set up one way to avoid circular dependencies

    | keys  | value type    |
    | :---: | :---:         |
    | cakupan    | [CakupanData][samudra.schemas.CakupanData] |
    """

    cakupan: CakupanData


class KataAsingData(FromPeeweeDatabase):
    """Object and JSONable representation of [models.KataAsing][samudra.models.core.kata_asing.KataAsing]

    | keys  | value type    |
    | :---: | :---:         |
    | id    | int |
    | nama  | str |
    | bahasa | str |
    """

    id: int
    nama: str
    bahasa: str


class KonsepToKataAsingConnector(FromPeeweeDatabase):
    """Object and JSONable representation of [models.KataAsingXKonsep][samudra.models.core.kata_asing.KataAsingXKonsep] with the exception that it is a one way connection.

    !!! note
        The connection has to be set up one way to avoid circular dependencies

    | keys  | value type    |
    | :---: | :---:         |
    | kata_asing    | [KataAsingData][samudra.schemas.KataAsingData] |
    """

    kata_asing: KataAsingData


class KonsepData(FromPeeweeDatabase):
    """Object and JSONable representation of [models.Konsep][samudra.models.core.konsep.Konsep].

    !!! important
        Because of the way the models have been set up, to get a single `cakupan` from `konsep` (Self) would be like so:
        ```python
        first_cakupan: CakupanData = Self.cakupan[0].cakupan
        ```
        It would seem like we are selecting `cakupan` twice but in fact we are first selecting a list of intermediate tables defined by [models.BaseAttachmentDataTable][samudra.models.base.BaseAttachmentDataTable].
        We then index into it (or iterate to get all) to reveal a data from [models.Cakupan][samudra.models.core.cakupan.Cakupan] table.
        The same can be said to find `kata_asing`.

        [## Schema of a Lemma][samudra.schemas--schema-of-a-lemma] gives a clearer picture of the data structure.

    | keys  | value type    |
    | :---: | :---:         |
    | id    | int |
    | keterangan  | str |
    | tertib | int (Optional) |
    | golongan  | [GolonganKataData][samudra.schemas.GolonganKataData] |
    | cakupan    | List[[KonsepToCakupanConnector][samudra.schemas.KonsepToCakupanConnector]] |
    | kata_asing    | List[[KonsepToKataAsingConnector][samudra.schemas.KonsepToKataAsingConnector]] |
    """

    id: int
    golongan: GolonganKataData
    keterangan: str
    tertib: Optional[int]
    cakupan: List[Optional[KonsepToCakupanConnector]]
    kata_asing: List[Optional[KataAsingData]]


class LemmaData(FromPeeweeDatabase):
    """Object and JSONable representation of [models.Lemma][samudra.models.core.lemma.Lemma]

    | keys  | value type    |
    | :---: | :---:         |
    | id    | int |
    | nama  | str |
    | konsep    | List[[KonsepData][samudra.schemas.KonsepData]] |
    """

    id: int
    nama: str
    konsep: List[KonsepData]
