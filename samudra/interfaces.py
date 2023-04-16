"""External applications are expected to interact with classes and functions defined here.

## Schemas

The module contains data schemas for use by external application

- [LemmaData][samudra.schemas.LemmaData]
- [KonsepData][samudra.schemas.KonsepData]
- [CakupanData][samudra.schemas.CakupanData]
- [KataAsingData][samudra.schemas.KataAsingData]
- [GolonganKataData][samudra.schemas.GolonganKataData]

## Builders

The module also contains data builders for use by external application

- [LemmaQueryBuilder][samudra.interfaces.LemmaQueryBuilder]
- [NewLemmaBuilder][samudra.interfaces.NewLemmaBuilder]
"""

from typing import List, Optional
from peewee import JOIN

import peewee as pw
from samudra import models
from samudra.schemas import (
    LemmaData,
    KonsepData,
    CakupanData,
    KataAsingData,
    KonsepToKataAsingConnector,
    GolonganKataData,
    KonsepToCakupanConnector,
)


class LemmaQueryBuilder:
    """A query builder to fetch lemma data and its relationships.

    !!! important
        If `lemma` and `konsep` is both `None`, it will raise a `ValueError`.

    Args:
        lemma (Optional[str], optional): The lemma to match to. Defaults to None.
        konsep (Optional[str], optional): The query contains these words in the konsep. Defaults to None.
    """

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
        """Fetch related `cakupan`.

        Returns:
            LemmaQueryBuilder: Returns self to continue building the query
        """
        self._query_stmt = self._query_stmt.join_from(
            models.Konsep, models.CakupanXKonsep, JOIN.LEFT_OUTER
        ).join(models.Cakupan, JOIN.LEFT_OUTER)
        return self

    def get_kata_asing(self) -> "LemmaQueryBuilder":
        """Fetch related `kata_asing`.

        Returns:
            LemmaQueryBuilder: Returns self to continue building the query
        """
        self._query_stmt = self._query_stmt.join_from(
            models.Konsep, models.KataAsingXKonsep, JOIN.LEFT_OUTER
        ).join(models.KataAsing, JOIN.LEFT_OUTER)
        return self

    def collect(self) -> Optional[LemmaData]:
        """Execute the query

        Returns:
            Optional[LemmaData]: Returns None if data matching query does not exist.
        """
        try:
            return LemmaData.from_orm(pw.prefetch(self._query_stmt.get()))
        except pw.DoesNotExist:
            return None


class NewLemmaBuilder:
    """A builder to insert new lemma and its related data

    Args:
        lemma (str): lemma name
        konsep (str): konsep detail
        golongan (str): existing [GolonganKata][samudra.models.core.konsep.GolonganKata]
    """

    def __init__(self, konsep: str, lemma: str, golongan: str) -> None:
        # TODO Fix dependence on first item tuple
        self.lemma = models.Lemma.get_or_create(nama=lemma)[0]
        self.golongan = models.GolonganKata.get(id=golongan)
        self.konsep = models.Konsep.get_or_create(
            lemma=self.lemma, golongan=self.golongan, keterangan=konsep
        )[0]

    def save(self) -> None:
        """Saves the data."""
        self.lemma.save()
        self.konsep.save()
        try:
            self.cakupan.save()
            self.cakupan_x_konsep.save()
        except AttributeError:
            pass
        try:
            self.kata_asing.save()
            self.kata_asing_x_konsep.save()
        except AttributeError:
            pass

    def set_cakupan(self, nama: str) -> "NewLemmaBuilder":
        """Attach the cakupan with the following nama

        Args:
            nama (str): cakupan name

        Returns:
            NewLemmaBuilder: Returns self to continue building
        """
        self.cakupan = models.Cakupan.get_or_create(nama=nama)[0]
        self.cakupan_x_konsep = models.CakupanXKonsep.get_or_create(
            cakupan=self.cakupan, konsep=self.konsep
        )[0]
        return self

    def set_kata_asing(self, nama: str, bahasa: str) -> "NewLemmaBuilder":
        """Attach the kata_asing with the following description

        Args:
            nama (str): foreign word
            bahasa (str): language of the word

        Returns:
            NewLemmaBuilder: Returns self to continue building
        """
        self.kata_asing = models.KataAsing.get_or_create(nama=nama, bahasa=bahasa)[0]
        self.kata_asing_x_konsep = models.KataAsingXKonsep.get_or_create(
            kata_asing=self.cakupan, konsep=self.konsep
        )[0]
        return self


def new_golongan_kata(id: str, nama: str, keterangan: str) -> models.GolonganKata:
    models.GolonganKata.create(id=id, nama=nama, keterangan=keterangan)
    return models.GolonganKata.get(id=id)
