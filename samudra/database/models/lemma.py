from peewee import AutoField, TextField, IntegerField, TimestampField, ForeignKeyField

from .base import Base


class Lemma(Base):
    """
    Lemma model
    """
    id = AutoField()
    tarikh_masuk = TimestampField()
    nama = TextField()
    golongan = TextField(null=False)
    konsep = TextField(null=True)
    nombor_semantik = IntegerField(null=True)


class LemmaAsing(Base):
    """
    Lemma bahasa asing
    """
    id = AutoField()
    tarikh_masuk = TimestampField()

    padanan_konsep = ForeignKeyField(Lemma, backref='lemma_asing')
    nama = TextField()
    golongan = TextField(null=False)