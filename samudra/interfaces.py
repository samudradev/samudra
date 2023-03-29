from typing import List
from peewee import JOIN

import peewee as pw
from samudra import models


class LemmaBuilder:
    _query_stmt = models.Lemma.select()

    def __init__(self, nama: str) -> None:
        self._query_stmt = self._query_stmt.where(models.Lemma.nama == nama)
        self.get_konsep()

    def get_konsep(self) -> "LemmaBuilder":
        self._query_stmt = self._query_stmt.join_from(
            models.Lemma, models.Konsep, JOIN.LEFT_OUTER
        )
        return self

    def get_cakupan(self) -> "LemmaBuilder":
        self._query_stmt = self._query_stmt.join_from(
            models.Konsep, models.CakupanXKonsep, JOIN.LEFT_OUTER
        ).join(models.Cakupan, JOIN.LEFT_OUTER)
        return self

    def get_kata_asing(self) -> "LemmaBuilder":
        self._query_stmt = self._query_stmt.join_from(
            models.Konsep, models.KataAsingXKonsep, JOIN.LEFT_OUTER
        ).join(models.KataAsing, JOIN.LEFT_OUTER)
        return self

    def query(self) -> List[models.Lemma]:
        return pw.prefetch(self._query_stmt)
