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
from typing import Dict, List, Optional, Set
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
    def __init__(self, data: LemmaData) -> None:
        self.data = data
        self.to_save: List[pw.Model] = []
        self.to_delete: List[pw.Model] = []

    def rename(self, new: str) -> "LemmaEditor":
        _lemma: models.Lemma = models.Lemma.get_by_id(self.data.id)
        _lemma.nama = new
        self.to_save.append(_lemma)
        return self

    def replace_konsep(self, index: int, keterangan: str) -> "LemmaEditor":
        _konsep: models.Konsep = models.Konsep.get_by_id(self.data.konsep[index].id)
        _konsep.keterangan = keterangan
        self.to_save.append(_konsep)
        return self

    def attach_cakupans(self, index: int, cakupans: List[str]) -> "LemmaEditor":
        _konsep: models.Konsep = models.Konsep.get_by_id(self.data.konsep[index].id)
        _cakupans: List[models.Cakupan] = _konsep.attach(
            # TODO USE get_or_init_record for lazy edit
            models.Cakupan,
            [{"nama": cakupan} for cakupan in cakupans],
        )
        self.to_save.extend(_cakupans)
        return self

    def detach_cakupans(self, index: int, cakupans: List[str]) -> "LemmaEditor":
        lookup = {
            connector.cakupan.nama: connector.cakupan
            for connector in self.data.konsep[index].cakupan
        }
        for cakupan in cakupans:
            to_remove = lookup[cakupan]
            record: models.CakupanXKonsep = models.CakupanXKonsep.get(
                cakupan=to_remove.id, konsep=self.data.konsep[index].id
            )
            self.to_delete.append(record)
        return self

    def save(self) -> None:
        while len(self.to_save) != 0:
            record = self.to_save.pop(0)
            record.update()
            record.save()

        while len(self.to_delete) != 0:
            self.to_delete.pop(0).delete_instance(recursive=False)


def get_or_init_record(model: pw.Model, *args, **kwargs) -> pw.Model:
    """Gets a record or initializes a new one without saving

    Args:
        model (pw.Model): A model

    Returns:
        pw.Model: Model instance
    """
    if data := model.get_or_none(*args, **kwargs) is None:
        data = model(*args, **kwargs)
    return data


class NewLemmaBuilder:
    """A builder to insert new lemma and its related data

    Args:
        lemma (str): lemma name
        konsep (str): konsep detail
        golongan (str): existing [GolonganKata][samudra.models.core.konsep.GolonganKata]
    """

    def __init__(self, konsep: str, lemma: str, golongan: str) -> None:
        self.lemma = get_or_init_record(models.Lemma, nama=lemma)
        self.golongan = models.GolonganKata.get(id=golongan)
        self.konsep = get_or_init_record(
            models.Konsep, lemma=self.lemma, golongan=self.golongan, keterangan=konsep
        )
        self.to_save: List[pw.Model] = [self.lemma, self.golongan, self.konsep]

    def save(self) -> None:
        """Saves the built record."""
        while len(self.to_save) != 0:
            record = self.to_save.pop(0)
            record.update()  # Fill previously NULL values
            record.save()

    def set_cakupan(self, nama: str) -> "NewLemmaBuilder":
        """Attach the cakupan with the following nama

        Args:
            nama (str): cakupan name

        Returns:
            NewLemmaBuilder: Returns self to continue building
        """
        self.cakupan = get_or_init_record(models.Cakupan, nama=nama)
        self.cakupan_x_konsep = get_or_init_record(
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
        self.kata_asing = get_or_init_record(models.KataAsing, nama=nama, bahasa=bahasa)
        self.kata_asing_x_konsep = get_or_init_record(
            models.KataAsingXKonsep, kata_asing=self.cakupan, konsep=self.konsep
        )
        self.to_save.extend([self.kata_asing, self.kata_asing_x_konsep])
        return self


def new_golongan_kata(id: str, nama: str, keterangan: str) -> models.GolonganKata:
    models.GolonganKata.create(id=id, nama=nama, keterangan=keterangan)
    return models.GolonganKata.get(id=id)
