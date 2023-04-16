from typing import List, Optional
from peewee import JOIN

import peewee as pw
from samudra import models
from samudra.internals import (
    LemmaData,
    KonsepData,
    CakupanData,
    KataAsingData,
    KonsepToKataAsingConnector,
    GolonganKataData,
    KonsepToCakupanConnector,
)


class LemmaQueryBuilder:
    _query_stmt = models.Lemma.select()

    def __init__(
        self, *, lemma: Optional[str] = None, konsep: Optional[str] = None
    ) -> None:
        if (lemma == None) and (konsep == None):
            whereclause = None
            raise ValueError(
                f"Please specify query. `lemma` dan `konsep` cannot both be None."
            )
        elif lemma and konsep:
            whereclause = models.Lemma.nama.contains(
                lemma
            ) or models.Konsep.keterangan.contains(konsep)
        elif lemma:
            whereclause = models.Lemma.nama.contains(lemma)
        elif konsep:
            whereclause = models.Konsep.keterangan.contains(konsep)

        self._query_stmt = (
            self._query_stmt.join_from(models.Lemma, models.Konsep, JOIN.LEFT_OUTER)
            .where(whereclause)
            .join_from(models.Konsep, models.GolonganKata, JOIN.LEFT_OUTER)
        )

    def get_cakupan(self) -> "LemmaQueryBuilder":
        self._query_stmt = self._query_stmt.join_from(
            models.Konsep, models.CakupanXKonsep, JOIN.LEFT_OUTER
        ).join(models.Cakupan, JOIN.LEFT_OUTER)
        return self

    def get_kata_asing(self) -> "LemmaQueryBuilder":
        self._query_stmt = self._query_stmt.join_from(
            models.Konsep, models.KataAsingXKonsep, JOIN.LEFT_OUTER
        ).join(models.KataAsing, JOIN.LEFT_OUTER)
        return self

    def collect(self) -> Optional[LemmaData]:
        try:
            return LemmaData.from_orm(pw.prefetch(self._query_stmt.get()))
        except pw.DoesNotExist:
            return None


class NewLemmaBuilder:
    def __init__(self, konsep: str, lemma: str, golongan: str) -> None:
        # TODO Fix dependence on first item tuple
        self.lemma = models.Lemma.get_or_create(nama=lemma)[0]
        self.golongan = models.GolonganKata.get(id=golongan)
        self.konsep = models.Konsep.get_or_create(
            lemma=self.lemma, golongan=self.golongan, keterangan=konsep
        )[0]

    def save(self) -> None:
        self.lemma.save()
        self.konsep.save()
        try:
            self.cakupan.save()
            self.cakupan_x_konsep.save()
        except AttributeError:
            pass

    def set_cakupan(self, nama: str) -> "NewLemmaBuilder":
        self.cakupan = models.Cakupan.get_or_create(nama=nama)[0]
        self.cakupan_x_konsep = models.CakupanXKonsep.get_or_create(
            cakupan=self.cakupan, konsep=self.konsep
        )[0]
        return self


def new_golongan_kata(id: str, nama: str, keterangan: str) -> models.GolonganKata:
    models.GolonganKata.create(id=id, nama=nama, keterangan=keterangan)
    return models.GolonganKata.get(id=id)
