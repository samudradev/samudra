from typing import Any

import peewee as pw
import pydantic as pyd
from pydantic.utils import GetterDict


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, pw.ModelSelect):
            return list(res)
        return res


class ORMSchema(pyd.BaseModel):
    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
