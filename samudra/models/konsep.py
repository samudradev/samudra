from peewee import AutoField, TextField, IntegerField, TimestampField, BlobField, ForeignKeyField

from .base import BaseTable
from .lemma import Lemma


class Konsep(BaseTable):
    """
    Konsep model
    """
    lemma = ForeignKeyField(model=Lemma, field=Lemma.id, backref='konsep', on_delete='cascade')
    golongan = TextField(null=False)
    keterangan = BlobField(null=True)
    # ---
    tertib = IntegerField(null=True)

    def __repr__(self):
        return f"<model.{self.__class__.__name__}: id={self.id} lemma={self.lemma} golongan={self.golongan} keterangan='{self.keterangan}'>"
