from peewee import BlobField, AutoField, TextField, ForeignKeyField

from .base import Base
from .. import Lemma


class Cakupan(Base):
    """
    Dalam konteks apakah istilah tersebut digunakan untuk konsep yang diberikan.
    """
    id = AutoField()
    nama = TextField(null=False)
    keterangan = BlobField(null=True)


class CakupanLemma(Base):
    cakupan = ForeignKeyField(model=Cakupan, field=Cakupan.id, backref='lemma')
    lemma = ForeignKeyField(model=Lemma, field=Lemma.id, backref='cakupan')