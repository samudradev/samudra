from peewee import AutoField, TimestampField, ForeignKeyField, TextField

from samudra.database import Lemma
from samudra.database.models.base import Base


class KataAsing(Base):
    """
    Lemma bahasa asing
    """
    id = AutoField()
    tarikh_masuk = TimestampField()

    padanan_konsep = ForeignKeyField(Lemma, backref='lemma_asing')
    nama = TextField(null=False)
    golongan = TextField(null=False)
