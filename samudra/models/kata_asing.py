from peewee import ForeignKeyField, TextField

from .base import BaseTable
from .konsep import Konsep


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
