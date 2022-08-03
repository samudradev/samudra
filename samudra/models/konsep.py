from peewee import AutoField, TextField, IntegerField, TimestampField, BlobField, ForeignKeyField, ModelSelect

from .base import BaseTable
from .lemma import Lemma


class Konsep(BaseTable):
    """
    Konsep model
    """
    lemma = ForeignKeyField(model=Lemma, field=Lemma.id, backref='konsep', on_delete='cascade')
    golongan = TextField(null=False)
    keterangan = TextField(null=True)
    # ---
    tertib = IntegerField(null=True)

    def __repr__(self):
        return f"<model.{self.__class__.__name__}: id={self.id} lemma={self.lemma} golongan={self.golongan} keterangan='{self.keterangan}'>"

    def attach_cakupan(self, *nama: str) -> ModelSelect:
        from . import Cakupan, CakupanXKonsep
        cakupan = [Cakupan.get_or_create(nama=nama_)[0] for nama_ in nama]
        for cakupan_ in cakupan:
            CakupanXKonsep.get_or_create(cakupan=cakupan_.id, konsep=self.id)
        return self.cakupan

    def attach_kata_asing(self, kata_asing: str, bahasa: str) -> ModelSelect:
        from samudra.models import KataAsing, KataAsingXKonsep
        kata_asing = KataAsing.get_or_create(nama=kata_asing, bahasa=bahasa)[0]
        KataAsingXKonsep.get_or_create(konsep=self.id, kata_asing=kata_asing.id)
        return self.kata_asing
