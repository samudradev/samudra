from peewee import AutoField, ForeignKeyField, TextField, BlobField

from .base import BaseTable
from samudra.database import Konsep


class JenisPerwakilanModen(BaseTable):
    keterangan = BlobField(null=True)


class PerwakilanModen(BaseTable):
    konsep = ForeignKeyField(model=Konsep, backref='perwakilan_moden')
    jenis = ForeignKeyField(model=JenisPerwakilanModen, backref='item')
    keterangan = TextField(null=False)
