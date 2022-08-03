from peewee import ForeignKeyField, TextField

from .base import BaseTable
from .konsep import Konsep


class KataAsing(BaseTable):
    """
    Lemma bahasa asing
    """
    nama = TextField(null=False)
    bahasa = TextField(null=False)


class KataAsingXKonsep(BaseTable):
    kata_asing = ForeignKeyField(KataAsing, field=KataAsing.id, backref='konsep', on_delete='cascade')
    konsep = ForeignKeyField(Konsep, field=Konsep.id, backref='kata_asing', on_delete='cascade')
