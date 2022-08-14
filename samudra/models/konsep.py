from typing import Dict, List

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

    def attach(self, to_model: BaseTable, through_model: BaseTable, values: List[Dict[str, str]]):
        get_or_create_values = [to_model.get_or_create(**key_val)[0] for key_val in values]
        model_name = to_model.__name__.lower()
        for value in get_or_create_values:
            through_model.get_or_create(**{model_name: value.id, self.__class__.__name__.lower(): self.id})
        return getattr(self, model_name)

    def attach_cakupan(self, *nama: str) -> ModelSelect:
        from . import Cakupan, CakupanXKonsep
        self.attach(to_model=Cakupan, through_model=CakupanXKonsep, values=[{'nama': nama_} for nama_ in nama])
        return self.cakupan

    def attach_kata_asing(self, kata_asing: str, bahasa: str) -> ModelSelect:
        from samudra.models import KataAsing, KataAsingXKonsep
        kata_asing = KataAsing.get_or_create(nama=kata_asing, bahasa=bahasa)[0]
        KataAsingXKonsep.get_or_create(konsep=self.id, kata_asing=kata_asing.id)
        return self.kata_asing
