from typing import Dict, List

from peewee import (
    AutoField,
    TextField,
    IntegerField,
    TimestampField,
    BlobField,
    ForeignKeyField,
    ModelSelect, CharField,
)

from models.base import BaseTable, BaseAttachmentTable, BaseRelationshipTable, BaseStrictTable
from .lemma import Lemma


class GolonganKata(BaseStrictTable):
    id = CharField(max_length=6, unique=True, null=False)
    nama = TextField(null=False)
    keterangan = TextField(null=False)


class Konsep(BaseTable):
    """
    Konsep model
    """

    lemma = ForeignKeyField(
        model=Lemma, field=Lemma.id, backref="konsep", on_delete="cascade"
    )
    # TODO: Create composite key of id and tertib
    # TODO: Point golongan to an external table with exhaustive list
    golongan = ForeignKeyField(model=GolonganKata, field=GolonganKata.id, on_delete='set null', null=True)
    keterangan = TextField(null=True, index=True)
    # ---
    tertib = IntegerField(null=True)

    def __repr__(self):
        return f"<model.{self.__class__.__name__}: id={self.id} lemma={self.lemma} golongan={self.golongan} keterangan='{self.keterangan}'>"

    def attach(self, to_model: BaseAttachmentTable, values: List[Dict[str, str]]):
        return to_model.__attach__(self, values=values)
