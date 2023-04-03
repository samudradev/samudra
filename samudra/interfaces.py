from typing import List
from peewee import JOIN

import peewee as pw
from samudra import models


class LemmaQueryBuilder:
    _query_stmt = models.Konsep.select()

    def __init__(self, konsep: str, lemma: str = None) -> None:
        self._query_stmt = (
            self._query_stmt.join_from(models.Konsep, models.Lemma, JOIN.LEFT_OUTER)
            .where(
                (models.Konsep.keterangan.contains(konsep))
                or (models.Lemma.nama.contains(lemma))
            )
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

    def collect(self) -> List[models.Konsep]:
        return pw.prefetch(self._query_stmt.get())


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


def new_golongan_kata(id: str, nama: str, keterangan: str) -> models.GolonganKata:
    models.GolonganKata.create(id=id, nama=nama, keterangan=keterangan)
    return models.GolonganKata.get(id=id)
