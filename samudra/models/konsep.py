from peewee import AutoField, TextField, IntegerField, TimestampField, BlobField, ForeignKeyField

from .base import BaseTable


class Lemma(BaseTable):
    """
    MODEL RELATIONSHIP REPRESENTATION
    .Lemma  <== .Konsep <== .Cakupan
                        <== .KataAsing
            <== .Ragam
    """
    nama = TextField(null=False)

    def __repr__(self) -> str:
        return f'<model.{self.__class__.__name__}: id={self.id} nama={self.nama}>'


class Ragam(BaseTable):
    baku = ForeignKeyField(model=Lemma, backref='ragam')
    ragam = ForeignKeyField(model=Lemma, backref='baku')


class Konsep(BaseTable):
    """
    Konsep model
    """
    lemma = ForeignKeyField(model=Lemma, field=Lemma.id, backref='konsep')
    golongan = TextField(null=False)
    keterangan = BlobField(null=True)
    # ---
    tertib = IntegerField(null=True)

    def __repr__(self):
        return f"<model.{self.__class__.__name__}: id={self.id} lemma={self.lemma} golongan={self.golongan} keterangan='{self.keterangan}'>"
