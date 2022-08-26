from peewee import BlobField, TextField, ForeignKeyField

from models.base import BaseTable, BaseAttachmentTable, BaseRelationshipTable
from .konsep import Konsep


class Cakupan(BaseAttachmentTable):
    """
    Dalam konteks apakah istilah tersebut digunakan untuk konsep yang diberikan.
    """

    nama = TextField(null=False, unique=True)
    keterangan = TextField(null=True)


class CakupanXKonsep(BaseRelationshipTable):
    cakupan = ForeignKeyField(
        model=Cakupan, field=Cakupan.id, backref="konsep", on_delete="cascade"
    )
    konsep = ForeignKeyField(
        model=Konsep, field=Konsep.id, backref="cakupan", on_delete="cascade"
    )


Cakupan.connection_table = CakupanXKonsep
