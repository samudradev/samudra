from peewee import AutoField, TextField, IntegerField, TimestampField, BlobField

from .base import Base


class Lemma(Base):
    """
    Lemma model
    """
    id = AutoField()
    tarikh_masuk = TimestampField()
    # ---
    nama = TextField(null=False)
    golongan = TextField(null=False)
    keterangan = BlobField(null=True)
    # ---
    nombor_semantik = IntegerField(null=True)
    tertib = IntegerField(null=True)


