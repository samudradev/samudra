from peewee import AutoField, TextField, IntegerField, TimestampField, BlobField

from .base import Base


class Konsep(Base):
    """
    Lemma model
    """
    id = AutoField()
    tarikh_masuk = TimestampField()
    # ---
    lemma = TextField(null=False)
    golongan = TextField(null=False)
    keterangan = BlobField(null=True)
    # ---
    nombor_semantik = IntegerField(null=True)
    tertib = IntegerField(null=True)

    def __repr__(self):
        return f"<model.Lemma: id={self.id} lemma={self.lemma} golongan={self.golongan}>"
