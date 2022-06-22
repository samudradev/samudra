from peewee import AutoField, CharField, TextField, IntegerField

from .base import Base


class Lemma(Base):
    """
    Lemma model
    """
    id_ = AutoField()
    nama = TextField()
    golongan = CharField(max_length=255)
    konsep = TextField(null=True)
    nombor_semantik = IntegerField(null=True)