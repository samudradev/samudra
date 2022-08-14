from peewee import TextField

from samudra.models.base import BaseTable


class Pengguna(BaseTable):
    nama = TextField(null=False)
    kunci = TextField(null=False)

    def __repr__(self) -> str:
        return f'<model.{self.__class__.__name__}: id={self.id} nama={self.nama} kunci={self.kunci}>'
