from typing import Dict, List

from peewee import (
    AutoField,
    TextField,
    IntegerField,
    TimestampField,
    BlobField,
    ForeignKeyField,
    ModelSelect,
)

from models.base import BaseTable, BaseMetadataTable, BaseConnectionTable
from .lemma import Lemma


class Konsep(BaseTable):
    """
    Konsep model
    """

    lemma = ForeignKeyField(
        model=Lemma, field=Lemma.id, backref="konsep", on_delete="cascade"
    )
    golongan = TextField(null=False)
    keterangan = TextField(null=True)
    # ---
    tertib = IntegerField(null=True)

    def __repr__(self):
        return f"<model.{self.__class__.__name__}: id={self.id} lemma={self.lemma} golongan={self.golongan} keterangan='{self.keterangan}'>"

    def attach(self, to_model: BaseMetadataTable, values: List[Dict[str, str]]):
        return to_model.__attach__(self, values=values)
