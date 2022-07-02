from peewee import AutoField, TimestampField, ForeignKeyField, TextField

from samudra.database import Konsep
from samudra.database.models.base import Base


class KataAsing(Base):
    """
    Lemma bahasa asing
    """
    id = AutoField()
    tarikh_masuk = TimestampField()
    lemma = TextField(null=False)
    golongan = TextField(null=False)


class PadananKonsepKeKataAsing(Base):
    konsep = ForeignKeyField(Konsep, backref='lemma_asing')
    kata_asing = ForeignKeyField(KataAsing, backref='konsep')
