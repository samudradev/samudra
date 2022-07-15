from peewee import BlobField, AutoField, TextField, ForeignKeyField, TimestampField

from .base import BaseTable
from .konsep import Konsep


class Cakupan(BaseTable):
    """
    Dalam konteks apakah istilah tersebut digunakan untuk konsep yang diberikan.
    """
    nama = TextField(null=False)
    keterangan = BlobField(null=True)


class CakupanKeKonsep(BaseTable):
    cakupan = ForeignKeyField(model=Cakupan, field=Cakupan.id, backref='konsep')
    konsep = ForeignKeyField(model=Konsep, field=Konsep.id, backref='cakupan')
