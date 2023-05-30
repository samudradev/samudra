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

from copy import deepcopy
from typing import List, Optional, Set
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


class LemmaEditor:
    def __init__(self, original: LemmaData) -> None:
        self.old = original
        self.new = deepcopy(original)

    def rename(self, new: str) -> "LemmaEditor":
        self.new.nama = new

    def rewrite_konsep(self, index: int, new: str) -> "LemmaEditor":
        self.new.konsep[index].keterangan = new

    def new_cakupan(self, index: int, cakupan: str) -> "LemmaEditor":
        cakupan_data = models.Cakupan.get_or_create(nama=cakupan)[0]

    # def add_konsep(self, konsep: KonsepData) -> "LemmaEditor":
    #     ...


class NewLemmaBuilder:
    """A builder to insert new lemma and its related data

    Args:
        lemma (str): lemma name
        konsep (str): konsep detail
        golongan (str): existing [GolonganKata][samudra.models.core.konsep.GolonganKata]
    """

    def __init__(self, konsep: str, lemma: str, golongan: str) -> None:
        # TODO Fix dependence on first item tuple
        self.lemma = self.get_or_new(models.Lemma, nama=lemma)
        self.golongan = models.GolonganKata.get(id=golongan)
        self.konsep = self.get_or_new(
            models.Konsep, lemma=self.lemma, golongan=self.golongan, keterangan=konsep
        )
        self.to_save: List[pw.Model] = [self.lemma, self.golongan, self.konsep]

    @staticmethod
    def get_or_new(model: pw.Model, *args, **kwargs) -> pw.Model:
        """Gets a record or initializes a new one without saving

        Args:
            model (pw.Model): A model

        Returns:
            pw.Model: Model instance
        """
        if data := model.get_or_none(*args, **kwargs) is None:
            data = model(*args, **kwargs)
        return data

    def save(self) -> None:
        """Saves the data."""
        for record in self.to_save:
            record.update()  # Fill previously NULL values
            record.save()

    def set_cakupan(self, nama: str) -> "NewLemmaBuilder":
        """Attach the cakupan with the following nama

        Args:
            nama (str): cakupan name

        Returns:
            NewLemmaBuilder: Returns self to continue building
        """
        self.cakupan = self.get_or_new(models.Cakupan, nama=nama)
        self.cakupan_x_konsep = self.get_or_new(
            models.CakupanXKonsep, cakupan=self.cakupan, konsep=self.konsep
        )
        self.to_save.extend([self.cakupan, self.cakupan_x_konsep])
        return self

    def set_kata_asing(self, nama: str, bahasa: str) -> "NewLemmaBuilder":
        """Attach the kata_asing with the following description

        Args:
            nama (str): foreign word
            bahasa (str): language of the word

        Returns:
            NewLemmaBuilder: Returns self to continue building
        """
        self.kata_asing = self.get_or_new(models.KataAsing, nama=nama, bahasa=bahasa)
        self.kata_asing_x_konsep = self.get_or_new(
            models.KataAsingXKonsep, kata_asing=self.cakupan, konsep=self.konsep
        )
        self.to_save.extend([self.kata_asing, self.kata_asing_x_konsep])
        return self


def new_golongan_kata(id: str, nama: str, keterangan: str) -> models.GolonganKata:
    models.GolonganKata.create(id=id, nama=nama, keterangan=keterangan)
    return models.GolonganKata.get(id=id)
