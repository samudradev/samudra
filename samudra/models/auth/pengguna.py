import enum

from peewee import TextField, BooleanField, ForeignKeyField

from samudra.models.base import BaseDataTable, BaseStrictDataTable


class RoleEnum(enum.Enum):
    DEFAULT = 'BIASA'


class Keizinan(BaseStrictDataTable):
    peranan = TextField(null=False, unique=True)
    baca = BooleanField(null=False)
    ubah = BooleanField(null=False)
    tambah = BooleanField(null=False)
    buang = BooleanField(null=False)


class Pengguna(BaseDataTable):
    nama = TextField(null=False)
    kunci = TextField(null=False)
    peranan = ForeignKeyField(model=Keizinan, field=Keizinan.peranan, backref='pengguna',
                              on_delete='set default', default=RoleEnum.DEFAULT.value)

    def __repr__(self) -> str:
        return f"<model.{self.__class__.__name__}: id={self.id} nama={self.nama} kunci={self.kunci}>"
