from pydantic import validator

from samudra.schemas.tables._helper import ORMSchema


class CreateGolonganKata(ORMSchema):
    id: str
    nama: str
    keterangan: str

    @validator('id')
    def id_must_be_less_than_six(cls, value: str):
        if len(value) > 6:
            raise ValueError('ID parameter must be less than 6 characters')
        return value.upper()

    @validator('nama')
    def nama_to_titlecase(cls, value: str):
        return value.title()
