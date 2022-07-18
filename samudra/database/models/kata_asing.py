from peewee import AutoField, TimestampField, ForeignKeyField, TextField

from .konsep import Konsep
from .base import BaseTable


class KataAsing(BaseTable):
    """
    Lemma bahasa asing
    """
    nama = TextField(null=False)
    golongan = TextField(null=False)
    bahasa = TextField(null=False)


class PadananKonsepKeKataAsing(BaseTable):
    konsep = ForeignKeyField(Konsep, backref='lemma_asing')
    kata_asing = ForeignKeyField(KataAsing, backref='konsep')
