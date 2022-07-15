import datetime

import pydantic as pyd


class KataAsingBase(pyd.BaseModel):
    lemma: str
    golongan: str


class KataAsingCreation(KataAsingBase):
    pass


class KataAsingRecord(KataAsingBase):
    # --- Record specific fields
    id: int
    tarikh_masuk: datetime.datetime

    class Config:
        orm_mode = True
